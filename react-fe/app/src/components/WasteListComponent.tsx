import React from 'react';
import { BinProphetRecord } from './BinProphetRecord';
interface WasteData {
  previsione_status: Date;
  riempimento: number;
  status: number;
}

interface WasteInfo {
  [key: string]: WasteData;
}

interface Props {
  wasteList: WasteInfo;
}

interface TypologyColorMap {
  vetro: string;
  plastica: string;
  carta: string;
  umido: string;
  other: string;
  [key: string]: string;
}

const typologyColorMap : TypologyColorMap = { "vetro": "bg-green-600", "plastica": "bg-blue-600", "carta": "bg-yellow-300", "umido": "bg-orange-900", "other": "bg-black-600" };


const WasteListComponent: React.FC<Props> = ({ wasteList }) => {
  if (!wasteList) return (<div className='text-bold'>Loading</div>);

  return (
    <div>
      {Object.keys(wasteList).map((wasteInfoKey, index) => {
      const wasteInfo = wasteList[wasteInfoKey as keyof WasteInfo];
        return (
          <div key={index}>
            <h3>Tipologia di rifiuto: {wasteInfoKey}</h3>
            <div>Stato: {wasteInfo.riempimento}</div>
            <BinProphetRecord filling={wasteInfo.riempimento} sort_type={wasteInfoKey} color={typologyColorMap[wasteInfoKey]} date={new Date(wasteInfo.previsione_status).toISOString()}></BinProphetRecord>
          </div>
        );
      })}
    </div>
  );
};

export default WasteListComponent;
