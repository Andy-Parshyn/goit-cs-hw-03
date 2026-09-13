-- 1. Всі завдання певного користувача
SELECT * FROM tasks WHERE user_id = 1;

-- 2. Завдання за статусом 'new' (підзапит)
SELECT * FROM tasks
WHERE status_id = (SELECT id FROM status WHERE name = 'new');

-- 3. Оновити статус конкретного завдання
UPDATE tasks
SET status_id = (SELECT id FROM status WHERE name = 'in progress')
WHERE id = 1;

-- 4. Користувачі без завдань
SELECT * FROM users
WHERE id NOT IN (SELECT user_id FROM tasks WHERE user_id IS NOT NULL);

-- 5. Додати нове завдання для користувача
INSERT INTO tasks (title, description, status_id, user_id)
VALUES ('Написати звіт', 'Звіт за тиждень', (SELECT id FROM status WHERE name = 'new'), 1);

-- 6. Незавершені завдання
SELECT * FROM tasks
WHERE status_id != (SELECT id FROM status WHERE name = 'completed');

-- 7. Видалити завдання за id
DELETE FROM tasks WHERE id = 2;

-- 8. Користувачі за email (LIKE)
SELECT * FROM users WHERE email LIKE '%@example.com';

-- 9. Оновити ім'я користувача
UPDATE users SET fullname = 'Іван Петренко' WHERE id = 1;

-- 10. Кількість завдань для кожного статусу
SELECT s.name, COUNT(t.id) AS tasks_count
FROM status s
LEFT JOIN tasks t ON t.status_id = s.id
GROUP BY s.name
ORDER BY s.name;

-- 11. Завдання користувачів з певним доменом email
SELECT t.*, u.email
FROM tasks t
JOIN users u ON u.id = t.user_id
WHERE u.email LIKE '%@example.com';

-- 12. Завдання без опису
SELECT * FROM tasks WHERE description IS NULL OR description = '';

-- 13. Користувачі та їхні завдання у статусі 'in progress'
SELECT u.fullname, t.title
FROM users u
INNER JOIN tasks t ON t.user_id = u.id
INNER JOIN status s ON s.id = t.status_id
WHERE s.name = 'in progress';

-- 14. Користувачі та кількість їхніх завдань
SELECT u.id, u.fullname, COUNT(t.id) AS tasks_count
FROM users u
LEFT JOIN tasks t ON t.user_id = u.id
GROUP BY u.id, u.fullname
ORDER BY u.id;
