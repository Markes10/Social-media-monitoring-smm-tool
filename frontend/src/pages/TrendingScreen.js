import React, { useState, useEffect } from "react";
import { View, Text, ScrollView } from "react-native";

const TrendingScreen = () => {
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    const ws = new WebSocket("ws://your-api-url/ws/alerts");

    ws.onmessage = (event) => {
      const newAlert = JSON.parse(event.data);
      setAlerts((prevAlerts) => [newAlert, ...prevAlerts]);
    };

    return () => ws.close();
  }, []);

  return (
    <View>
      <Text>Real-Time Trending Alerts:</Text>
      <ScrollView>
        {alerts.map((alert, index) => (
          <Text key={index}>
            🔥 {alert.topic} - Mentions: {alert.mentions} - Sentiment: {alert.sentiment}
          </Text>
        ))}
      </ScrollView>
    </View>
  );
};

export default TrendingScreen;
