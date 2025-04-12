-- Представление клиентов с возрастом и длительностью использования
create or replace view v_customers_with_age_duration as
select 
    c.cardholder_id as customer_key,
    c.first_name,
    c.last_name,
    c.gender,
    c.birth_date,
    c.occupation,
    c.account_type,
    date_part('year', age(current_date, c.birth_date)) as age,
    current_date - min(cast(t.start_time as date)) as duration
from transactions t
join customers c on t.cardholder_id = c.cardholder_id
group by c.cardholder_id, c.first_name, c.last_name, c.gender, c.birth_date, c.occupation, c.account_type;

-- Представление с полной информацией о транзакциях
create or replace view v_transactions as
select
    t.transaction_id,
    t.start_time,
    t.end_time,
    t.cardholder_id,
    c.first_name,
    c.last_name,
    c.gender,
    c.occupation,
    c.birth_date,
    c.account_type,
    c.is_wisabi,
    t.location_id,
    a.location_name,
    a.city,
    a.state,
    a.country,
    t.transaction_type_id,
    tt.transaction_desc,
    t.amount,
    t.region
from transactions t
left join customers c on t.cardholder_id = c.cardholder_id
left join atm_location a on t.location_id = a.location_id
left join transaction_type tt on t.transaction_type_id = tt.transaction_type_id;

-- Количество транзакций по полу
create or replace view v_transaction_count_gender as
select 
    c.gender, 
    count(t.transaction_id) as transaction_count
from transactions t
join customers c on t.cardholder_id = c.cardholder_id
group by c.gender;

-- Общая сумма транзакций по полу
create or replace view v_transaction_amount_gender as
select 
    c.gender, 
    sum(t.amount) as total_amount
from transactions t
join customers c on t.cardholder_id = c.cardholder_id
group by c.gender;

-- Сумма транзакций по регионам
create or replace view v_transaction_amount_region as
select 
    t.region, 
    sum(t.amount) as total_amount
from transactions t
group by t.region;

-- Количество транзакций по регионам
create or replace view v_transaction_count_region as
select 
    t.region, 
    count(t.transaction_id) as transaction_count
from transactions t
group by t.region;

-- Топ-10 клиентов по сумме транзакций
create or replace view v_top_clients as
select 
    c.cardholder_id, 
    c.first_name || ' ' || c.last_name as full_name, 
    sum(t.amount) as total_amount
from transactions t
join customers c on t.cardholder_id = c.cardholder_id
group by c.cardholder_id, full_name
order by total_amount desc
limit 10;

-- Средняя сумма транзакции по профессиям
create or replace view v_avg_transaction_by_occupation as
select 
    c.occupation, 
    avg(t.amount) as avg_transaction
from transactions t
join customers c on t.cardholder_id = c.cardholder_id
group by c.occupation;

-- Сумма транзакций по типу банковского счёта
create or replace view v_transaction_amount_by_account_type as
select 
    c.account_type, 
    sum(t.amount) as total_amount
from transactions t
join customers c on t.cardholder_id = c.cardholder_id
group by c.account_type;

-- Распределение транзакций по дням недели
create or replace view v_transaction_by_weekday as
select 
    cal.day_name,
    count(t.transaction_id) as transaction_count,
    sum(t.amount) as total_amount
from transactions t
join calendar cal on cast(t.start_time as date) = cal.date
where cal.day_name is not null
group by cal.day_name
order by array_position(['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'], cal.day_name);

-- Возраст клиентов и сумма транзакций
create or replace view v_transaction_age_group as
select 
    date_part('year', age(current_date, c.birth_date)) as age,
    sum(t.amount) as total_amount
from transactions t
join customers c on t.cardholder_id = c.cardholder_id
where c.birth_date is not null
group by age
order by age;

-- Транзакции по часам
create or replace view v_transaction_by_hour as
select 
    extract(hour from t.start_time) as hour,
    count(t.transaction_id) as transaction_count,
    sum(t.amount) as total_amount
from transactions t
group by hour
order by hour;
