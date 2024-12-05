# PostScore Project - bitPin

This project involves designing and implementing a Django application using Django REST Framework (DRF) to enable users to view and rate posts. Each post includes a title and content, and the list view must display the title, the number of users who have rated the post, the average rating, rating_count, and, if applicable, the user’s own rating. The application must efficiently handle high volumes, including millions of ratings per post and thousands of requests per second. Users can submit or update their ratings (ranging from 0 to 5). Additionally, a mechanism must be implemented to mitigate the impact of sudden, biased, or mass ratings caused by external influences, such as social campaigns. The project emphasizes scalability, performance optimization.

## Features:

__User Authentication__: Secure login and registration for sellers and administrators using JWT token.

 __Post System :__

- **PostListView (APIView) :**
A Django Rest Framework (DRF) APIView that handles requests for posts.
Supports both GET (to fetch posts with ratings) and POST (to create a new post) methods.

- **PostLogic :**
Contains the business logic for posts.
Handles interactions between the views and the data layer (PostDao).

- **PostDao :**
Data Access Object (DAO) for database operations related to posts and ratings.
Fetches posts with related ratings and user-specific data.
Caches the results of the query to improve performance.


__Rating System :__

This module provides the logic and data access for a rating system where users can rate posts. It ensures fairness by applying rate-limiting, deviation checks, and weighted scoring based on the time interval between ratings.


- **RatingLogic:** 
  - Handles the business logic for the rating system. The RatingLogic class encapsulates the core functionality of the rating system, including:

  - Ensuring users can't rate posts too frequently.

  - Validating ratings to avoid extreme deviations from the average.

  - Calculating weighted scores based on the time elapsed since the user's last rating.


- **RatingDao:**
Manages database operations related to ratings.






__Rate Limiting:__

- Prevents users from rating the same post multiple times within 30 seconds.

__Deviation Check:__

- Ensures user ratings are not significantly different from the average score.
Uses standard deviation to determine allowable range:
If std_dev == 0: Deviation limit is ±2.
Otherwise: Deviation limit is ±2 * std_dev.

__Weighted Scoring:__

- Applies a weight of 0 if the time elapsed since the last rating is ≤10 minutes (rating ignored).
Applies a weight of 1 otherwise (rating accepted).

__Caching:__

- Invalidates the cache for the posts list when a rating is updated to ensure consistency.


__DataBase Models:__

- Post: Represents a post with fields like title and content.

- Rating: Represents a user's rating for a post, with fields like score and relationships to Post and User.

