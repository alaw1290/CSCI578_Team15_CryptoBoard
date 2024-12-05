import React from "react";
import { useNavigate, Link } from "react-router-dom";
import Toolbar, { Item, ToolbarTypes } from "devextreme-react/toolbar";

const Navbar: React.FC = () => {
  const navigate = useNavigate();

  const onItemClick = (e: ToolbarTypes.ItemClickEvent) => {
    if (e.itemData?.options.text) {
      if (e.itemData.options.text !== "Currencies") {
        navigate(`/${e.itemData.options.text.toLowerCase()}`);
      } else {
        navigate("/");
      }
    } else {
      navigate("/");
    }
  };

  return (
    <div className="navbar">
      <Toolbar onItemClick={onItemClick}>
        <Item location="before" options={homeOptions}>
          <Link to="/">
            <span className="navbar-brand">CryptoBoard</span>
          </Link>
        </Item>
        <Item
          widget="dxButton"
          location="before"
          locateInMenu="auto"
          options={homeOptions}
        />
        <Item
          widget="dxButton"
          location="before"
          locateInMenu="auto"
          options={predictionOptions}
        />
        <Item
          widget="dxButton"
          location="before"
          locateInMenu="auto"
          options={sentimentsOptions}
        />
      </Toolbar>
    </div>
  );
};

const homeOptions = {
  text: "Currencies",
  stylingMode: "text",
};

const predictionOptions = {
  text: "Predictions",
  stylingMode: "text",
};

const sentimentsOptions = {
  text: "Sentiments",
  stylingMode: "text",
};

export default Navbar;
