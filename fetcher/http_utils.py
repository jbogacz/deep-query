"""HTTP utilities for API requests with retry logic."""

import time

import httpx


def make_request_with_retry(
    client: httpx.Client, method: str, url: str, max_retries: int = 3, **kwargs
) -> httpx.Response:
    """Make a request with retry logic for rate limiting."""

    for attempt in range(max_retries + 1):
        try:
            response = client.request(method, url, **kwargs)

            # Check for rate limiting
            if response.status_code == 429:
                if attempt == max_retries:
                    response.raise_for_status()  # Let the final attempt raise the error

                # Extract wait time from response if available
                retry_after = response.headers.get("Retry-After")
                if retry_after:
                    wait_time = int(retry_after)
                else:
                    # Exponential backoff: 1s, 2s, 4s
                    wait_time = 2**attempt

                print(
                    f"Rate limited on {method} {url} (attempt {attempt + 1}/{max_retries + 1}). Waiting {wait_time} seconds..."
                )
                time.sleep(wait_time)
                continue

            response.raise_for_status()
            return response

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                if attempt == max_retries:
                    raise

                # Check response text for rate limit message
                response_text = e.response.text.lower()
                if (
                    "too many requests" in response_text
                    or "rate limit" in response_text
                ):
                    # Exponential backoff
                    wait_time = 2**attempt
                    print(
                        f"Rate limited on {method} {url} (attempt {attempt + 1}/{max_retries + 1}). Waiting {wait_time} seconds..."
                    )
                    time.sleep(wait_time)
                    continue

            # Non-rate-limit HTTP error - print stack trace and raise
            import traceback

            print(f"HTTP error occurred (status {e.response.status_code}):")
            print(f"Request URL: {e.request.url}")
            print(f"Response text: {e.response.text}")
            print("Stack trace:")
            traceback.print_exc()
            raise
        except httpx.RequestError as e:
            if attempt == max_retries:
                # Network error on final attempt - print stack trace and raise
                import traceback

                print(f"Network error occurred after {max_retries + 1} attempts:")
                print(f"Request URL: {e.request.url}")
                print(f"Error: {e}")
                print("Stack trace:")
                traceback.print_exc()
                raise

            # Network error - retry with exponential backoff
            wait_time = 2**attempt
            print(
                f"Network error (attempt {attempt + 1}/{max_retries + 1}). Retrying in {wait_time} seconds..."
            )
            time.sleep(wait_time)
            continue
        except Exception as e:
            # Unexpected error - print stack trace and raise
            import traceback

            print(f"Unexpected error occurred:")
            print(f"Error: {e}")
            print("Stack trace:")
            traceback.print_exc()
            raise

    raise Exception("Max retries exceeded")
