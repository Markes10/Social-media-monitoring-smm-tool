const fetchFakeNewsPosts = async () => {
    try {
      const response = await axios.get("http://your-api-url/get_fake_news_posts");
      setFlaggedPosts(response.data.fake_news_posts);
    } catch (error) {
      console.error("Error fetching fake news posts:", error);
    }
};
