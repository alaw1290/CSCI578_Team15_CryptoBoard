import React, { useState, useEffect } from "react";
import TabPanel, { Item } from "devextreme-react/tab-panel";
import SentimentsDataGrid from "../components/SentimentsDataGrid";

interface SentimentData {
  crypto_name: string;
  id: string;
  published_date: number;
  sentiment: number;
  source: string;
  summary: string;
  title: string;
  url: string;
}

const Sentiments: React.FC = () => {
  const [bitcoinData, setBitcoinData] = useState<SentimentData[] | null>(null);
  const [dogecoinData, setDogecoinData] = useState<SentimentData[] | null>(
    null
  );
  const [tetherData, setTetherData] = useState<SentimentData[] | null>(null);
  const [ethereumData, setEthereumData] = useState<SentimentData[] | null>(
    null
  );
  const [solanaData, setSolanaData] = useState<SentimentData[] | null>(null);

  const fetchData = async (
    endpoint: string,
    setState: React.Dispatch<React.SetStateAction<SentimentData[] | null>>
  ) => {
    try {
      const response = await fetch(endpoint);
      const data = await response.json();
      setState(data);
    } catch (error) {
      console.error(`Error fetching data from ${endpoint}:`, error);
      setState(null);
    }
  };

  useEffect(() => {
    fetchData("http://127.0.0.1:8000/1/articles", setBitcoinData);
    fetchData("http://127.0.0.1:8000/74/articles", setDogecoinData);
    fetchData("http://127.0.0.1:8000/825/articles", setTetherData);
    fetchData("http://127.0.0.1:8000/1027/articles", setEthereumData);
    fetchData("http://127.0.0.1:8000/5426/articles", setSolanaData);
  }, []);

  return (
    <div className="tab-panel">
      <h4>Cryptocurrency Sentiments</h4>
      <TabPanel defaultSelectedIndex={0}>
        <Item title="Bitcoin">
          <div className="tab-text">
            {bitcoinData ? (
              <SentimentsDataGrid data={bitcoinData} />
            ) : (
              <p>Loading Bitcoin sentiment data...</p>
            )}
          </div>
        </Item>
        <Item title="Dogecoin">
          <div className="tab-text">
            {dogecoinData ? (
              <SentimentsDataGrid data={dogecoinData} />
            ) : (
              <p>Loading Dogecoin sentiment data...</p>
            )}
          </div>
        </Item>
        <Item title="Tether">
          <div className="tab-text">
            {tetherData ? (
              <SentimentsDataGrid data={tetherData} />
            ) : (
              <p>Loading Tether sentiment data...</p>
            )}
          </div>
        </Item>
        <Item title="Ethereum">
          <div className="tab-text">
            {ethereumData ? (
              <SentimentsDataGrid data={ethereumData} />
            ) : (
              <p>Loading Ethereum sentiment data...</p>
            )}
          </div>
        </Item>
        <Item title="Solana">
          <div className="tab-text">
            {solanaData ? (
              <SentimentsDataGrid data={solanaData} />
            ) : (
              <p>Loading Solana sentiment data...</p>
            )}
          </div>
        </Item>
      </TabPanel>
    </div>
  );
};

export default Sentiments;
