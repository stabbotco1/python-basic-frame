# This is a thread-safe, double-checked singleton implementation.

How it works:

If no logger exists, it locks execution (_lock) and creates a new logger.
Thread-Safe Lock: Ensures that only one thread can create the logger.
Double-checked Locking: Prevents multiple threads from creating the logger simultaneously.
If the logger already exists, it is returned immediately.
