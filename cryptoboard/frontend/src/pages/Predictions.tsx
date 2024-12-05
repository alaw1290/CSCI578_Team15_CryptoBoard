import React, { useState, useEffect } from "react";
import TabPanel, { Item } from "devextreme-react/tab-panel";
import CryptoPredictionChart from "../components/CryptoPredictionChart";

interface PredictionsData {
  "1h_prediction": number;
  "12h_prediction": number;
  "24h_prediction": number;
  "7d_prediction": number;
}

const Predictions: React.FC = () => {
  const [bitcoinPredictions, setBitcoinPredictions] = useState<PredictionsData | null>(null);
  const [dogecoinPredictions, setDogecoinPredictions] = useState<PredictionsData | null>(null);
  const [tetherPredictions, setTetherPredictions] = useState<PredictionsData | null>(null);
  const [ethereumPredictions, setEthereumPredictions] = useState<PredictionsData | null>(null);
  const [solanaPredictions, setSolanaPredictions] = useState<PredictionsData | null>(null);

  useEffect(() => {
    const fetchPredictions = async (endpoint: string, setState: React.Dispatch<React.SetStateAction<PredictionsData | null>>) => {
      try {
        const response = await fetch(`http://localhost:8000/${endpoint}/prediction`);
        const data = await response.json();
        setState(data);
      } catch (error) {
        console.error(`Error fetching predictions from ${endpoint}:`, error);
      }
    };

    fetchPredictions("1", setBitcoinPredictions);
    fetchPredictions("74", setDogecoinPredictions);
    fetchPredictions("825", setTetherPredictions);
    fetchPredictions("1027", setEthereumPredictions);
    fetchPredictions("5426", setSolanaPredictions);
  }, []);

  return (
    <div className="tab-panel">
      <h4>Cryptocurrency Predictions</h4>
      <TabPanel defaultSelectedIndex={0}>
        <Item title="Bitcoin">
          <div className="tab-text">
            {bitcoinPredictions ? (
              <CryptoPredictionChart predictions={bitcoinPredictions} />
            ) : (
              <p>Loading Bitcoin predictions...</p>
            )}
            <p>
              Explore the future price predictions for Bitcoin over different intervals like 1 hour, 12 hours, 24 hours, and 7 days.
            </p>
          </div>
        </Item>
        <Item title="Dogecoin">
          <div className="tab-text">
            {dogecoinPredictions ? (
              <CryptoPredictionChart predictions={dogecoinPredictions} />
            ) : (
              <p>Loading Dogecoin predictions...</p>
            )}
            <p>
              Check out Dogecoin's price predictions for various time intervals, powered by advanced machine learning models.
            </p>
          </div>
        </Item>
        <Item title="Tether">
          <div className="tab-text">
            {tetherPredictions ? (
              <CryptoPredictionChart predictions={tetherPredictions} />
            ) : (
              <p>Loading Tether predictions...</p>
            )}
            <p>
              See how Tether's price might evolve in the near future with predictions over short- and long-term intervals.
            </p>
          </div>
        </Item>
        <Item title="Ethereum">
          <div className="tab-text">
            {ethereumPredictions ? (
              <CryptoPredictionChart predictions={ethereumPredictions} />
            ) : (
              <p>Loading Ethereum predictions...</p>
            )}
            <p>
              Ethereum price predictions are available here, offering insights into how its value might change over time.
            </p>
          </div>
        </Item>
        <Item title="Solana">
          <div className="tab-text">
            {solanaPredictions ? (
              <CryptoPredictionChart predictions={solanaPredictions} />
            ) : (
              <p>Loading Solana predictions...</p>
            )}
            <p>
              Discover the potential price movements of Solana with our detailed prediction charts for various intervals.
            </p>
          </div>
        </Item>
      </TabPanel>
    </div>
  );
};

export default Predictions;
