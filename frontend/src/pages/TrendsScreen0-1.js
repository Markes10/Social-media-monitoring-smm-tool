import React, { useEffect, useState } from "react";
import { View, Text, FlatList } from "react-native";
import { PieChart } from "react-native-chart-kit";
import axios from "axios";

const TrendsScreen = () => {
    const [sentimentData, setSentimentData] = useState([]);
    const [trendingData, setTrendingData] = useState({ hashtags: [], keywords: [] });

    useEffect(() => {
        fetchSentimentTrends();
        fetchTrendingData();
    }, []);

    const fetchSentimentTrends = async () => {
        try {
            const response = await axios.get("http://your-api-url/get_sentiment_trends");
            const data = response.data.trends.map((item) => ({
                name: item.sentiment,
                population: item.count,
                color: item.sentiment === "positive" ? "green" : item.sentiment === "negative" ? "red" : "gray",
                legendFontColor: "#7F7F7F",
                legendFontSize: 15,
            }));
            setSentimentData(data);
        } catch (error) {
            console.error("Error fetching sentiment trends:", error);
        }
    };

    const fetchTrendingData = async () => {
        try {
            const response = await axios.get("http://your-api-url/get_trending_data");
            setTrendingData(response.data);
        } catch (error) {
            console.error("Error fetching trending data:", error);
        }
    };

    return (
        <View>
            <Text style={{ fontSize: 20, fontWeight: "bold", textAlign: "center", marginBottom: 10 }}>
                📊 Trends Overview
            </Text>
            
            <Text style={{ fontSize: 18, fontWeight: "bold" }}>📈 Sentiment Analysis Trends</Text>
            <PieChart
                data={sentimentData}
                width={300}
                height={220}
                chartConfig={{ backgroundColor: "#e26a00", color: () => "black" }}
                accessor="population"
                backgroundColor="transparent"
            />

            <Text style={{ fontSize: 18, fontWeight: "bold", marginTop: 10 }}>🔥 Trending Hashtags</Text>
            <FlatList
                data={trendingData.hashtags}
                keyExtractor={(item) => item.hashtag}
                renderItem={({ item }) => <Text>#{item.hashtag} ({item.count})</Text>}
            />

            <Text style={{ fontSize: 18, fontWeight: "bold", marginTop: 10 }}>🔑 Trending Keywords</Text>
            <FlatList
                data={trendingData.keywords}
                keyExtractor={(item) => item.keyword}
                renderItem={({ item }) => <Text>{item.keyword} ({item.count})</Text>}
            />
        </View>
    );
};

export default TrendsScreen;
