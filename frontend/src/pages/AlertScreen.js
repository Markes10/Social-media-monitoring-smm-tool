import React, { useEffect, useState } from "react";
import { View, Text, FlatList, StyleSheet } from "react-native";
import axios from "axios";

const AlertScreen = () => {
  const [negativePosts, setNegativePosts] = useState([]);

  useEffect(() => {
    fetchNegativePosts();
  }, []);

  const fetchNegativePosts = async () => {
    try {
      const response = await axios.get("http://your-api-url/get_negative_posts");
      setNegativePosts(response.data.negative_posts);
    } catch (error) {
      console.error("Error fetching negative posts:", error);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.header}>🚨 Negative Posts Alerts</Text>
      <FlatList
        data={negativePosts}
        keyExtractor={(item, index) => index.toString()}
        renderItem={({ item }) => (
          <View style={styles.card}>
            <Text style={styles.postText}>{item.text}</Text>
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
  postText: { fontSize: 16 },
});

export default AlertScreen;
