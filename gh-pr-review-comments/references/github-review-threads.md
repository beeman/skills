# GitHub Review Thread Commands

Use this reference only when you need concrete GitHub CLI commands for replies or thread resolution.

## Fetch Authoritative Review Comments

Fetch the live PR review comments with REST:

```bash
gh api --paginate repos/$OWNER/$REPO/pulls/$PR/comments
```

Treat this response as the source of truth for review comments. Do not rely on screenshots.

This endpoint returns reply comments as well as thread-start comments. Filter out items with `in_reply_to_id` before triaging so replies are not treated as separate review requests.

## Map Comment IDs to Thread IDs

GitHub resolves review threads by GraphQL thread ID, not REST comment ID. Use GraphQL when you need to resolve a thread.

`databaseId` in the GraphQL response maps to the REST comment `id`.

```bash
gh api graphql \
  -f owner="$OWNER" \
  -f repo="$REPO" \
  -F number="$PR" \
  -f after="$AFTER" \
  -f query='
query($owner: String!, $repo: String!, $number: Int!, $after: String) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      reviewThreads(first: 100, after: $after) {
        pageInfo {
          hasNextPage
          endCursor
        }
        nodes {
          id
          isResolved
          comments(first: 100) {
            pageInfo {
              hasNextPage
              endCursor
            }
            nodes {
              databaseId
              url
            }
          }
        }
      }
    }
  }
}'
```

Use the returned `id` for the thread mutation and `databaseId` to match the thread to a REST comment.

This example fetches a single GraphQL page. If the PR may exceed 100 review threads, continue paging `reviewThreads` with `pageInfo` and `after` cursors until all target REST comment IDs are mapped or there are no more pages. If a single thread may exceed 100 comments, paginate that thread's `comments` connection before treating the mapping as complete.

## Reply to a Review Comment

Reply before resolving every handled thread, including fixed comments:

```bash
gh api \
  -X POST \
  "repos/$OWNER/$REPO/pulls/$PR/comments/$COMMENT_ID/replies" \
  -f body='Rationale for the resolution'
```

Keep the reply short, concrete, and specific to the code or tradeoff.

## Request Human Review Again

Re-request human review after the fix is pushed when the reviewer was identified from the handled review comments:

```bash
gh api \
  -X POST \
  "repos/$OWNER/$REPO/pulls/$PR/requested_reviewers" \
  -f reviewers[]="$REVIEWER_LOGIN"
```

Prefer the review-comment author login as the reviewer identity. If GitHub rejects the request because the reviewer cannot be requested, do not guess at another reviewer.

## Resolve a Review Thread

Resolve the thread only after the fix or rationale is in place:

```bash
gh api graphql \
  -f threadId="$THREAD_ID" \
  -f query='
mutation($threadId: ID!) {
  resolveReviewThread(input: {threadId: $threadId}) {
    thread {
      id
      isResolved
    }
  }
}'
```

Use the response to confirm `isResolved` is `true`.

## Practical Order

Use this order when handling a thread:

1. Decide whether the comment is accepted, optional, or rejected.
2. Apply the code change first if the comment is accepted.
3. Post a short reply describing the action taken.
4. Resolve the thread with the GraphQL mutation.
