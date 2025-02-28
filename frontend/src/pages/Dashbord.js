import React, { useState } from "react";
import { Container, Box, Button, AppBar, Toolbar, IconButton, Typography } from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import Sidebar from "../components/Sidebar";
import DataTable from "../components/DataTable";
import SentimentChart from "../components/SentimentChart";
import SentimentBarChart from "../components/SentimentBarChart";
import CompetitorSentimentChart from "../components/CompetitorSentimentChart";
import TrendingHashtags from "../components/TrendingHashtags";
import KeywordSentiment from "../components/KeywordSentiment";
import DownloadReport from "../components/DownloadReport";
import LiveUpdates from "../components/LiveUpdates";
import { analyzeSentiment } from "../api";

const Dashboard = () => {
    const [sidebarOpen, setSidebarOpen] = useState(false);

    const handleAnalyze = async () => {
        await analyzeSentiment();
        window.location.reload();
    };

    return (
        <Container>
            {/* Navbar */}
            <AppBar position="static">
                <Toolbar>
                    <IconButton edge="start" color="inherit" onClick={() => setSidebarOpen(true)}>
                        <MenuIcon />
                    </IconButton>
                    <Typography variant="h6">SMM Dashboard</Typography>
                </Toolbar>
            </AppBar>
            
            {/* Sidebar */}
            <Sidebar open={sidebarOpen} onClose={() => setSidebarOpen(false)} />

            {/* Live Updates Section */}
            <Box sx={{ mt: 2 }}>
                <LiveUpdates />
            </Box>

            {/* Controls */}
            <Box sx={{ textAlign: "right", mt: 2 }}>
                <Button variant="contained" color="primary" onClick={handleAnalyze}>Analyze Sentiment</Button>
                <DownloadReport />
            </Box>

            {/* Analytics */}
            <DataTable />
            <SentimentChart />
            <SentimentBarChart />
            <CompetitorSentimentChart />
            <TrendingHashtags />
            <KeywordSentiment />
        </Container>
    );
};

export default Dashboard;