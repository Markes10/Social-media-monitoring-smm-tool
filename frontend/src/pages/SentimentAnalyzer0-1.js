import React, { useState } from "react";
import { View, Text, TextInput, Button, StyleSheet } from "react-native";
import axios from "axios";

const SentimentAnalyzer = () => {
  const [text, setText] = useState("");
  const [sentiment, setSentiment] = useState(null);
  const [engagement, setEngagement] = useState(null);

  const analyzeSentiment = async () => {
    try {
      const response = await axios.post("http://your-api-url/analyze_sentiment", { text });
      setSentiment(response.data);
    } catch (error) {
      console.error("Error analyzing sentiment:", error);
    }
  };

  const predictEngagement = async () => {
    try {
      if (sentiment) {
        const response = await axios.post("http://your-api-url/predict_engagement", {
          polarity: sentiment.polarity,
        });
        setEngagement(response.data);
      }
    } catch (error) {
      console.error("Error predicting engagement:", error);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.header}>📊 Sentiment & Engagement Analysis</Text>
      <TextInput
        style={styles.input}
        placeholder="Enter Post Text"
        value={text}
        onChangeText={setText}
      />
      <Button title="Analyze Sentiment" onPress={analyzeSentiment} />
      {sentiment && (
        <Text style={styles.result}>
          Sentiment: {sentiment.sentiment} (Polarity: {sentiment.polarity.toFixed(2)})
        </Text>
      )}
      <Button title="Predict Engagement" onPress={predictEngagement} />
      {engagement && (
        <Text style={styles.result}>
          Likes: {engagement.predicted_likes}, Shares: {engagement.predicted_shares},
          Comments: {engagement.predicted_comments}
        </Text>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: { padding: 20, backgroundColor: "#fff" },
  header: { fontSize: 22, fontWeight: "bold", marginBottom: 10 },
  input: { borderWidth: 1, padding: 10, marginVertical: 10, borderRadius: 5 },
  result: { fontSize: 16, marginTop: 10, fontWeight: "bold" },
});

export default SentimentAnalyzer;
