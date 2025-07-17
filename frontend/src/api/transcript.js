import axios from 'axios';

export const fetchTranscript = async (url) => {
  try {
    const response = await axios.post('http://localhost:8000/api/transcript/fetch', { url });
    return response.data;
  } catch (error) {
    console.error('Error fetching transcript:', error);
    return [];
  }
};
