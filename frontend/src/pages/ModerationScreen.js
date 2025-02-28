import React, { useEffect, useState } from "react";
import { View, Text, FlatList, Button, StyleSheet } from "react-native";
import axios from "axios";

const ModerationScreen = () => {
  const [flaggedPosts, setFlaggedPosts] = useState([]);

  useEffect(() => {
    fetchFlaggedPosts();
  }, []);

  const fetchFlaggedPosts = async () => {
    try {
      const response = await axios.get("http://your-api-url/get_flagged_posts");
      setFlaggedPosts(response.data.flagged_posts);
    } catch (error) {
      console.error("Error fetching flagged posts:", error);
    }
  };

  const moderatePost = async (postId, action) => {
    try {
      await axios.post("http://your-api-url/moderate_post", {
        post_id: postId,
        action: action,
      });
      fetchFlaggedPosts(); // Refresh after moderation
    } catch (error) {
      console.error("Error moderating post:", error);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.header}>🚨 Flagged Posts</Text>
      <FlatList
        data={flaggedPosts}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <View style={styles.card}>
            <Text style={styles.postText}>{item.text}</Text>
            <View style={styles.buttonRow}>
              <Button title="Approve" onPress={() => moderatePost(item.id, "approve")} />
              <Button title="Reject" color="red" onPress={() => moderatePost(item.id, "reject")} />
            </View>
          </View>
        )}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: { padding: 20, backgroundColor: "#fff" },
  header: { fontSize: 22, fontWeight: "bold", marginBottom: 10 },
  card: { padding: 15, backgroundColor: "#ffcccc", marginVertical: 5, borderRadius: 5 },
  postText: { fontSize: 16, marginBottom: 10 },
  buttonRow: { flexDirection: "row", justifyContent: "space-between" },
});

export default ModerationScreen;
