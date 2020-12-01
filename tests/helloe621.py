import py621


tags = ["protogen", "anthro"]

# Get a list of safe posts with the tags contained in the above list and don't check for tag validity
SamplePosts = py621.public.getPosts(True, tags, 10, 1, False)

SamplePost = SamplePosts[0] # Select the first post from the list

print("Post ID:")
print(SamplePost["id"]) # Print the post's ID

print("Post URL:")
print(SamplePost["file"]["url"]) # Print the post's media URL