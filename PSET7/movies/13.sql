SELECT name FROM people WHERE name != "Kevin Bacon" AND name IN (SELECT DISTINCT person_id FROM stars WHERE movie_id IN (SELECT movie_id FROM stars WHERE person_id IN (SELECT id FROM people WHERE name = "kevin Bacon" AND birth = "1958")))

-- SELECT name FROM people WHERE name != "Kevin Bacon" AND id IN (SELECT DISTINCT person_id FROM stars JOIN people ON stars.movie_id = people.id WHERE )