/* Query used for slide 1*/ 
SELECT sub.category_name, sub.duration_quartile, COUNT(sub.duration_quartile)
FROM (
    SELECT f.title title, 
           c.name category_name,
           f.rental_duration rental_duration,
           NTILE(4) OVER (ORDER BY f.rental_duration) AS duration_quartile
    FROM film f
    JOIN film_category fc 
    ON fc.film_id = f.film_id
    JOIN category c
    ON c.category_id = fc.category_id
    WHERE c.name in ('Animation', 'Children', 'Classics', 'Comedy', 'Family', 'Music')) sub
GROUP BY 1,2
ORDER BY 1,2


/* Query used for slide 2*/ 
WITH t1 AS (
    SELECT DATE_PART('month', r.rental_date) AS month,
           DATE_PART('year', r.rental_date) AS year,
           s2.store_id AS store_id, 
           COUNT(r.rental_id) AS num_rentals
    FROM rental r 
    JOIN staff s1 
    ON r.staff_id = s1.staff_id
    JOIN store s2 
    ON s2.store_id = s1.store_id
    GROUP BY 1,2,3
    ORDER BY 1,2)

SELECT month, store_id, num_rentals
FROM t1
WHERE year = 2005


/* Query used for slide 3*/ 
WITH t1 AS (
    SELECT (c.first_name || ' ' || c.last_name) AS customer_name, 
            c.customer_id, 
            p.amount, 
            DATE_PART('month', p.payment_date) AS payment_month, 
            DATE_PART('year', p.payment_date) AS payment_year
    FROM customer AS c
    JOIN payment AS p
    ON c.customer_id = p.customer_id),

    t2 AS (SELECT t1.payment_month, 
                  t1.customer_name, 
                  SUM(t1.amount) AS pay_amount
           FROM t1
           WHERE t1.payment_year = 2007
           GROUP BY 1,2
           ORDER BY 1, 3 DESC)

SELECT DISTINCT ON (payment_month)
       payment_month, 
       customer_name, 
       pay_amount AS max_pay_amount
FROM   t2


/* Query used for slide 4*/ 
WITH t1 AS (
    SELECT (c.first_name || ' ' || c.last_name) AS customer_name, 
            c.customer_id, 
            p.amount, 
            DATE_PART('month', p.payment_date) AS payment_month, 
            DATE_PART('year', p.payment_date) AS payment_year
    FROM customer AS c
    JOIN payment AS p
    ON c.customer_id = p.customer_id),

    vip AS (
        SELECT t1.customer_id
        FROM t1
        GROUP BY 1
        ORDER BY SUM(t1.amount) DESC
        LIMIT 10),
     
    t2 AS (
        SELECT t1.payment_year,
               t1.payment_month,
               t1.customer_name,
               COUNT (*) AS pay_count,
               SUM(t1.amount) AS pay_amount
        FROM t1
        JOIN vip
        ON t1.customer_id = vip.customer_id
        WHERE t1.payment_year = 2007
        GROUP BY 1,2,3)

SELECT  t2.customer_name,
        t2.payment_month,
        t2.pay_amount,
        LAG(t2.pay_amount) OVER(PARTITION BY t2.customer_name ORDER BY t2.payment_month) AS lag,
        t2.pay_amount - LAG(t2.pay_amount) OVER(PARTITION BY t2.customer_name ORDER BY t2.payment_month) AS lag_diff
FROM t2