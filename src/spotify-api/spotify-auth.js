const axios = require('axios');
const qs = require('qs');

const clientId = '67dc3d054c744ea1a0e7f532cf53c4ee';
const clientSecret = '25823d4675db4cb0a5ea6f1c6bbea956';

const authHeader = Buffer.from(`${clientId}:${clientSecret}`).toString('base64');

const getToken = async () => {
  const tokenUrl = 'https://accounts.spotify.com/api/token';
  const headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': `Basic ${authHeader}`
  };
  const data = qs.stringify({
    'grant_type': 'client_credentials'
  });

  try {
    const response = await axios.post(tokenUrl, data, { headers });
    console.log('Access Token:', response.data.access_token);
    return response.data.access_token;
  } catch (error) {
    console.error('Error fetching token:', error.response ? error.response.data : error.message);
  }
};

getToken();