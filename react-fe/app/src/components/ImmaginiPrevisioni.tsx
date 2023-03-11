import React from 'react';

export interface base64Previsions {
    [key: string]: string  }

  
interface Props {
    previsioni: base64Previsions;
}

const ImmaginiPrevisioni: React.FC<Props> = ({ previsioni }) => {
    if(!previsioni) return (<div>loading</div>);
    return (
        <div>
            {Object.keys(previsioni).map((key:string, index) => (

                <img key={index} src={`data:image/png;base64,${previsioni[key]}`} alt={key} />
            ))}
        </div>
    );
};
//                 <span key={index}> {key} {previsioni[key]} </span>


export default ImmaginiPrevisioni;
