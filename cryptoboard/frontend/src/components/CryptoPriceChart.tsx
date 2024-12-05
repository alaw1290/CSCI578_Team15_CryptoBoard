import React from "react";
import {
  Chart,
  Series,
  ArgumentAxis,
  Export,
  Legend,
  Margin,
  Tooltip,
  Grid,
} from "devextreme-react/chart";

interface CryptoPriceChartProps {
  data: {
    price: string;
    timestamp: number;
    name: string;
  }[];
}

const CryptoPriceChart: React.FC<CryptoPriceChartProps> = ({ data }) => {
  const filteredData = data
    .filter((_, index) => index % 2 === 0)
    .map((item) => ({
      ...item,
      formattedTimestamp: new Date(item.timestamp * 1000).toLocaleString(),
      price: parseFloat(item.price),
    }));

  const getCryptoName = () => {
    if (data.length > 0) {
      return `${data[0].name} Price`;
    }
    return "Crypto Price";
  };

  return (
    <div>
      <Chart id="chart" dataSource={filteredData} title={getCryptoName()}>
        <Series
          valueField="price"
          argumentField="formattedTimestamp"
          name="Price"
          type="line"
        />
        <ArgumentAxis valueMarginsEnabled={false} />
        <Margin bottom={20} />
        <Export enabled={true} />
        <Legend visible={false} />
        <Tooltip enabled={true} />
        <Grid visible={true} />
      </Chart>
    </div>
  );
};

export default CryptoPriceChart;
