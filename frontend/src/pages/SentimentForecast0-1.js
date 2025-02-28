import React, { useState } from "react";
import { View, Text, TextInput, Button, FlatList, StyleSheet } from "react-native";
import axios from "axios";

const SentimentForecast = () => {
    const [input, setInput] = useState("");
    const [forecast, setForecast] = useState([]);
    const [prediction, setPrediction] = useState(null);

    const fetchPrediction = async () => {
        const response = await axios.get(`http://your-api-url/predict_sentiment?brand=${input}`);
        setPrediction(response.data);
    };

    const fetchForecast = async () => {
        const res = await axios.get(`http://your-api-url/forecast_sentiment?topic=${input}`);
        setForecast(res.data.forecast);
    };

    return (
        <View style={styles.container}>
            <Text style={styles.header}>🔮 Sentiment Forecast</Text>

            <TextInput
                placeholder="Enter a brand or topic"
                value={input}
                onChangeText={setInput}
                style={styles.input}
            />

            <Button title="🔍 Predict Sentiment" onPress={fetchPrediction} />
            <Button title="📊 Forecast Future Sentiment" onPress={fetchForecast} />

            {prediction && (
                <Text style={styles.result}>
                    {prediction.sentiment_trend === "Negative" 
                        ? `⚠️ Warning: ${input} may face a negative trend!`
                        : `✅ Good News: ${input} sentiment is stable!`}
                </Text>
            )}

            <FlatList
                data={forecast}
                keyExtractor={(item) => item.ds}
                renderItem={({ item }) => (
                    <View style={styles.forecastItem}>
                        <Text>{item.ds} 📅</Text>
                        <Text>Predicted Sentiment: {item.yhat > 0 ? "😊 Positive" : item.yhat < 0 ? "😡 Negative" : "😐 Neutral"}</Text>
                    </View>
                )}
            />
        </View>
    );
};

const styles = StyleSheet.create({
    container: { padding: 20 },
    header: { fontSize: 20, fontWeight: "bold", marginBottom: 10 },
    input: { borderWidth: 1, padding: 10, marginBottom: 10 },
    result: { fontSize: 16, marginTop: 10, fontWeight: "bold" },
    forecastItem: { marginTop: 10 }
});

export default SentimentForecast;
