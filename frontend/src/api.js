import axios from "axios";

const API_URL = "http://localhost:8000/api";

export const fetchPosts = async (platform = "", startDate = "", endDate = "") => {
    const params = {};
    if (platform) params.platform = platform;
    if (startDate && endDate) {
        params.start_date = startDate;
        params.end_date = endDate;
    }
    const response = await axios.get(`${API_URL}/posts`, { params });
    return response.data;
};

export const analyzeSentiment = async () => {
    const response = await axios.get(`${API_URL}/analyze`);
    return response.data;
};

export const fetchCompetitorData = async (brands, startDate = "", endDate = "") => {
    const params = { brands: brands.join(",") };
    if (startDate && endDate) {
        params.start_date = startDate;
        params.end_date = endDate;
    }
    const response = await axios.get(`${API_URL}/competitor-analysis`, { params });
    return response.data;
};

export const fetchTrendingHashtags = async (platform = "", startDate = "", endDate = "") => {
    const params = {};
    if (platform) params.platform = platform;
    if (startDate && endDate) {
        params.start_date = startDate;
        params.end_date = endDate;
    }
    const response = await axios.get(`${API_URL}/hashtags`, { params });
    return response.data;
};

export const fetchKeywordAnalysis = async (keyword) => {
    const response = await axios.get(`${API_URL}/keyword-analysis`, { params: { keyword } });
    return response.data;
};

export const downloadReport = async () => {
    const response = await axios.get(`${API_URL}/generate-report`, { responseType: "blob" });
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", "SMM_Report.pdf");
    document.body.appendChild(link);
    link.click();
};
