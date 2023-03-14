import React from 'react';
import { BinProphetRecord } from './BinProphetRecord';
import { GreenCircle, RedCircle, YellowCircle } from './icons/Circles';
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

const typologyColorMap: TypologyColorMap = { "vetro": "bg-green-600", "plastica": "bg-blue-600", "carta": "bg-yellow-300", "umido": "bg-orange-900", "other": "bg-black-600" };


const WasteListComponent: React.FC<Props> = ({ wasteList }) => {
  if (!wasteList) return (<div className='text-bold'>Loading</div>);

  return (
    <div>
      {Object.keys(wasteList).map((wasteInfoKey, index) => {
        const wasteInfo = wasteList[wasteInfoKey as keyof WasteInfo];
        return (
          <div key={index}>
            <hr></hr>
            <div className='font-medium mb-4 mt-2'>
              Tipologia rifiuto:  <span className='uppercase'>{wasteInfoKey}</span></div>
            <div className='mb-4'>Stato: {wasteInfo.status === 1 ? <span> <GreenCircle></GreenCircle> OK!</span> : wasteInfo.status == 2 ? <span><YellowCircle></YellowCircle> FULL!</span> : <span> <RedCircle></RedCircle> DANGER!</span>}</div>
            <BinProphetRecord filling={wasteInfo.riempimento} sort_type={wasteInfoKey} color={typologyColorMap[wasteInfoKey]} date={String(wasteInfo.previsione_status)}></BinProphetRecord>
          </div>
        );
      })}
    </div>
  );
};

export default WasteListComponent;
