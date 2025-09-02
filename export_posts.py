import json
import os
import sys
from datetime import datetime
from atproto import Client

def export_posts_to_json(handle):
    """
    Fetches all posts from an atproto account and saves them to a timestamped JSON file.

    Args:
        handle: The atproto handle (e.g., 'user.bsky.social')

    This includes the post text, creation date, and public URLs for any images.
    No authentication required - fetches public posts only.
    """
    client = Client()
    
    print(f"🔍 Resolving handle: {handle}")
    
    # Resolve handle to DID without authentication
    try:
        identity_response = client.com.atproto.identity.resolve_handle({'handle': handle})
        repo_did = identity_response.did
        print(f"✅ Found DID: {repo_did}")
    except Exception as e:
        print(f"❌ Error resolving handle '{handle}': {e}")
        print("💡 Make sure the handle is correct (e.g., user.bsky.social)")
        return
    
    # Create timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"{handle}_posts_{timestamp}.json"
    
    all_posts = []
    cursor = None
    posts_fetched = 0
    
    # The CDN URL for Bluesky images.
    image_cdn_base = "https://cdn.bsky.app/img/feed_fullsize/plain"

    print("Starting to fetch posts... This may take a while if you have many posts.")

    while True:
        try:
            # list_records is the key function here. We're asking for records
            # in the 'app.bsky.feed.post' collection.
            response = client.com.atproto.repo.list_records(
                {
                    'repo': repo_did,
                    'collection': 'app.bsky.feed.post',
                    'limit': 100,  # Fetch 100 posts at a time
                    'cursor': cursor,
                }
            )
            
            if not response.records:
                print("No more posts found.")
                break

            for record in response.records:
                post_data = {
                    'created_at': record.value.created_at,
                    'text': record.value.text,
                    'images': []
                }

                # Check for and process embedded images
                if hasattr(record.value, 'embed') and record.value.embed:
                    # The '$type' field tells us what kind of embed it is
                    if record.value.embed.py_type == 'app.bsky.embed.images':
                        for image in record.value.embed.images:
                            image_url = f"{image_cdn_base}/{repo_did}/{image.image.cid}@jpeg"
                            post_data['images'].append({
                                'url': image_url,
                                'alt_text': image.alt
                            })
                
                all_posts.append(post_data)

            posts_fetched += len(response.records)
            print(f"Fetched {posts_fetched} posts so far...")
            
            # The cursor is our bookmark to get the next page of results.
            cursor = response.cursor
            if not cursor:
                print("Reached end of data.")
                break
                
        except Exception as e:
            print(f"An error occurred: {e}")
            break

    # Sort posts by creation date (newest first)
    if all_posts:
        all_posts.sort(key=lambda x: x['created_at'], reverse=True)
    
    # Write the collected data to a JSON file
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(all_posts, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Export complete!")
    print(f"📊 Total posts exported: {len(all_posts)}")
    print(f"💾 Export saved to: {output_filename}")


if __name__ == '__main__':
    # Check command line arguments
    if len(sys.argv) < 2:
        print("🦋 Bluesky Posts Export Tool")
        print("=" * 40)
        print("Usage: python export_posts.py <handle>")
        print("")
        print("Examples:")
        print("  python export_posts.py symm.social")
        print("  python export_posts.py user.bsky.social")
        print("")
        print("Each export gets a unique timestamp in the filename.")
        print("")
        print("🔓 No authentication required - exports public posts only.")
        exit(1)
    
    handle = sys.argv[1]
    
    print(f"🎯 Target account: {handle}")
    print(f"📥 Starting full export (no authentication)...")
        
    export_posts_to_json(handle)