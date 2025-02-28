import React, { useState } from "react";
import { View, Text, TextInput, Button } from "react-native";
import axios from "axios";

const HashtagInsightsDashboard = () => {
    const [hashtag, setHashtag] = useState("");
    const [data, setData] = useState(null);

    const fetchHashtagInsights = async () => {
        const res = await axios.get(`http://your-api-url/hashtag_insights/${hashtag}`);
        setData(res.data);
    };

    return (
        <View>
            <Text>🔍 Hashtag Sentiment Analysis</Text>
            <TextInput 
                placeholder="Enter Hashtag (e.g., #AI)" 
                value={hashtag} 
                onChangeText={setHashtag}
            />
            <Button title="Analyze" onPress={fetchHashtagInsights} />

            {data && (
                <View>
                    <Text>📢 Hashtag: {data.hashtag}</Text>
                    <Text>📊 Sentiment Score: {data.sentiment_score}</Text>
                </View>
            )}
        </View>
    );
};

export default HashtagInsightsDashboard;
