SELECT title FROM movies JOIN stars ON movies.id = stars.movie_id JOIN people ON stars.movie_id = people.id WHERE name LIKE "Bradley Cooper" AND "Jennifer Lawrence"