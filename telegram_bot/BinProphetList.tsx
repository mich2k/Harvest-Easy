import { BinProphetRecord } from "../react-fe/app/src/components/BinProphetRecord";
import React from "react";



interface Props {
    previsione_status: Date;  // ETA Filling date
    riempimento: number;    // Actual Filling percentage
    status: number;         // FSM status
  }



export const BinProphetList = ({ msg: apartmentPrevisions }) => {
    return (
        <div>
            {Object.keys(apartmentPrevisions).map((key: string, index) => (
                console.log(key, previsioni[key]);
            ))}
            <BinProphetRecord color={typologyColorMap[type].length === 0 ? typologyColorMap["other"] : typologyColorMap[type]} date="test" sort_type="test_tip" filling={parseFloat("0.95")} />
        </div>

    );

}