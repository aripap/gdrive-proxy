export default {
  async fetch(request) {
    // Extract file ID from URL
    let url = new URL(request.url);
    let fileId = url.pathname.replace("/", "");

    // If no file ID provided, return an error
    if (!fileId) {
      return new Response("File ID is required.", { status: 400 });
    }

    // Construct the Google Drive direct download URL
    let gdriveUrl = `https://drive.google.com/uc?export=download&id=${fileId}`;

    try {
      // Fetch the Google Drive file
      let response = await fetch(gdriveUrl, {
        headers: { "User-Agent": "Mozilla/5.0" } // Pretend to be a browser
      });

      // If Google blocks it, return an error
      if (!response.ok) {
        return new Response("Failed to fetch Google Drive file.", { status: 500 });
      }

      // Return the video file with correct headers
      return new Response(response.body, {
        status: 200,
        headers: {
          "Content-Type": "video/mp4",
          "Access-Control-Allow-Origin": "*", // Allows embedding in MRSS players
          "Cache-Control": "public, max-age=3600" // Cache the request for 1 hour
        }
      });

    } catch (error) {
      return new Response("Server error.", { status: 500 });
    }
  }
};
