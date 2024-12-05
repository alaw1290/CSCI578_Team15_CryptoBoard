import React, { useState, useEffect } from "react";
import TabPanel, { Item } from "devextreme-react/tab-panel";
import CryptoPriceChart from "../components/CryptoPriceChart";

export interface data {
  circulating_supply: string;
  coinmarket_id: number;
  infinite_supply: boolean;
  market_cap: string;
  max_supply: number;
  name: string;
  percent_change_1h: string;
  percent_change_7d: string;
  percent_change_24h: string;
  percent_change_30d: string;
  price: string;
  slug: string;
  symbol: string;
  timestamp: number;
  total_supply: string;
  volume_24h: string;
}

const Currencies: React.FC = () => {
  const [bitcoin, setBitcoin] = useState<data[] | null>(null);
  const [dogecoin, setDogecoin] = useState<data[] | null>(null);
  const [tether, setTether] = useState<data[] | null>(null);
  const [ethereum, setEthereum] = useState<data[] | null>(null);
  const [solana, setSolana] = useState<data[] | null>(null);

  const fetchData = async (
    endpoint: string,
    setState: React.Dispatch<React.SetStateAction<data[] | null>>
  ) => {
    try {
      const response = await fetch(`http://localhost:8000/${endpoint}/data`);
      const data = await response.json();
      setState(data);
    } catch (error) {
      console.error(`Error fetching data from ${endpoint}:`, error);
      setState(null);
    }
  };

  useEffect(() => {
    fetchData("1", setBitcoin);
    fetchData("74", setDogecoin);
    fetchData("825", setTether);
    fetchData("1027", setEthereum);
    fetchData("5426", setSolana);
  }, []);

  return (
    <div className="tab-panel">
      <h4>Cryptocurrency Prices</h4>
      <TabPanel defaultSelectedIndex={0}>
        <Item title="Bitcoin">
          <div className="tab-text">
            {bitcoin ? (
              <CryptoPriceChart data={bitcoin} />
            ) : (
              <p>Loading Bitcoin data...</p>
            )}
            <p>
              Bitcoin is a decentralized digital currency, without a central
              bank or single administrator, that can be sent from user to user
              on the peer-to-peer bitcoin network without the need for
              intermediaries.
            </p>
          </div>
        </Item>
        <Item title="Dogecoin">
          <div className="tab-text">
            {dogecoin ? (
              <CryptoPriceChart data={dogecoin} />
            ) : (
              <p>Loading Dogecoin data...</p>
            )}
            <p>
              Dogecoin is a cryptocurrency invented by software engineers Billy
              Markus and Jackson Palmer, who decided to create a payment system
              that is instant, fun, and free from traditional banking fees.
            </p>
          </div>
        </Item>
        <Item title="Tether">
          <div className="tab-text">
            {tether ? (
              <CryptoPriceChart data={tether} />
            ) : (
              <p>Loading Tether data...</p>
            )}
            <p>
              Tether is a blockchain-based cryptocurrency whose cryptocoins in
              circulation are backed by an equivalent amount of traditional fiat
              currencies, like the dollar, the euro, or the Japanese yen, which
              are held in a designated bank account.
            </p>
          </div>
        </Item>
        <Item title="Ethereum">
          <div className="tab-text">
            {ethereum ? (
              <CryptoPriceChart data={ethereum} />
            ) : (
              <p>Loading Ethereum data...</p>
            )}
            <p>
              Ethereum is a decentralized, open-source blockchain with smart
              contract functionality. Ether is the native cryptocurrency of the
              platform. After Bitcoin, it is the largest cryptocurrency by
              market capitalization.
            </p>
          </div>
        </Item>
        <Item title="Solana">
          <div className="tab-text">
            {solana ? (
              <CryptoPriceChart data={solana} />
            ) : (
              <p>Loading Solana data...</p>
            )}
            <p>
              Solana is a high-performance blockchain supporting builders around
              the world. It's fast, secure, and censorship-resistant. Solana
              features a suite of decentralized applications and protocols that
              provide easy, composable building blocks.
            </p>
          </div>
        </Item>
      </TabPanel>
    </div>
  );
};

export default Currencies;
