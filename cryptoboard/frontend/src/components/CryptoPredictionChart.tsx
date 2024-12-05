import React from "react";
import {
  Chart,
  Series,
  ArgumentAxis,
  Export,
  Legend,
  Margin,
  Title,
  Tooltip,
  Grid,
} from "devextreme-react/chart";

interface CryptoPredictionChartProps {
  predictions: {
    "1h_prediction": number;
    "12h_prediction": number;
    "24h_prediction": number;
    "7d_prediction": number;
  };
}

const CryptoPredictionChart: React.FC<CryptoPredictionChartProps> = ({
  predictions,
}) => {
  const formattedData = Object.entries(predictions).map(([key, value]) => ({
    interval: key.replace("_prediction", ""),
    prediction: value,
  }));

  return (
    <div>
      <div>Crypto Price Predictions</div>
      <Chart
        id="prediction-chart"
        dataSource={formattedData}
        title="Price Predictions"
      >
        <Series
          valueField="prediction"
          argumentField="interval"
          name="Prediction"
          type="bar" // Change to "line" for a line chart
        />
        <ArgumentAxis valueMarginsEnabled={true} />
        <Margin bottom={20} />
        <Export enabled={true} />
        <Legend visible={false} />
        <Title text="Price Predictions for Different Intervals" />
        <Tooltip enabled={true} />
        <Grid visible={true} />
      </Chart>
    </div>
  );
};

export default CryptoPredictionChart;
