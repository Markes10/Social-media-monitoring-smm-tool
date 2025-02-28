import React, { useState } from "react";
import { View, TextInput, Button, Text, ScrollView } from "react-native";
import axios from "axios";

const SentimentScreen = () => {
  const [text, setText] = useState("");
  const [sentiment, setSentiment] = useState("");

  const analyzeSentiment = async () => {
    try {
      const res = await axios.post("http://your-api-url/analyze_sentiment", { text });
      setSentiment(JSON.stringify(res.data.sentiment, null, 2));
    } catch (error) {
      console.error("Sentiment Analysis Error:", error);
      setSentiment("Error analyzing sentiment.");
    }
  };

  return (
    <View>
      <Text>Enter text for sentiment analysis:</Text>
      <TextInput 
        placeholder="Type a comment, tweet, or post..." 
        value={text} 
        onChangeText={setText} 
        style={{ borderWidth: 1, padding: 8, marginBottom: 10 }} 
      />
      <Button title="Analyze Sentiment" onPress={analyzeSentiment} />
      <ScrollView style={{ marginTop: 10 }}>
        <Text>{sentiment}</Text>
      </ScrollView>
    </View>
  );
};

export default SentimentScreen;
