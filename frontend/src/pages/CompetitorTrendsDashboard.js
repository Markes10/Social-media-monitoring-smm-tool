import React, { useState } from "react";
import { View, Text, Button } from "react-native";
import axios from "axios";

const CompetitorTrendsDashboard = () => {
    const [data, setData] = useState(null);

    const fetchCompetitorTrends = async () => {
        const res = await axios.get("http://your-api-url/competitor_trends");
        setData(res.data);
    };

    return (
        <View>
            <Text>📊 Competitor Trend Analysis</Text>
            <Button title="🔍 Fetch Trends" onPress={fetchCompetitorTrends} />

            {data && (
                <View>
                    <Text>🔥 Top Trends: {JSON.stringify(data.competitor_trends)}</Text>
                </View>
            )}
        </View>
    );
};

export default CompetitorTrendsDashboard;
