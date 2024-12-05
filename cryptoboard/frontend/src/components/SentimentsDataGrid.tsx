import React from "react";
import DataGrid, {
  Column,
  GroupPanel,
  Pager,
  Paging,
  Sorting,
} from "devextreme-react/data-grid";

interface SentimentsDataGridProps {
  data: {
    crypto_name: string;
    id: string;
    published_date: number;
    sentiment: number;
    source: string;
    summary: string;
    title: string;
    url: string;
  }[];
}

const SentimentsDataGrid: React.FC<SentimentsDataGridProps> = ({ data }) => {
  const filteredData = data.filter((item) => item.title && item.url);
  const numberOfArticles = filteredData.length;
  const averageSentiment =
    filteredData.reduce((sum, item) => sum + item.sentiment, 0) /
    (numberOfArticles || 1);

  return (
    <>
      <div className="summary">
        <h4>Summary</h4>
        <p>Number of Articles: {numberOfArticles}</p>
        <p>Average Sentiment: {averageSentiment.toFixed(2)}</p>
      </div>
      <DataGrid
        dataSource={filteredData}
        showBorders={true}
        columnAutoWidth={true}
        allowColumnResizing={true}
        allowColumnReordering={true}
        rowAlternationEnabled={true}
      >
        <GroupPanel visible={true} />
        <Sorting mode="multiple" />
        <Paging defaultPageSize={15} />
        <Pager
          showPageSizeSelector={true}
          allowedPageSizes={[15, 30, 50]}
          showInfo={true}
        />

        {/* Columns */}
        <Column dataField="crypto_name" caption="Crypto Name" />
        <Column dataField="source" caption="Source" groupIndex={0} />
        <Column dataField="sentiment" caption="Sentiment" />
        <Column
          dataField="title"
          caption="Article Title"
          cellRender={(cellData) => (
            <a
              href={cellData.data.url}
              target="_blank"
              rel="noopener noreferrer"
            >
              {cellData.value}
            </a>
          )}
        />
        <Column dataField="summary" caption="Summary" />
      </DataGrid>
    </>
  );
};

export default SentimentsDataGrid;
