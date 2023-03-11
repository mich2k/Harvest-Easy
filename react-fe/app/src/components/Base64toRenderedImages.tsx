import React from 'react';

export interface base64Previsions {
    [key: string]: string
}


interface Props {
    previsioni: base64Previsions;
}

function capitalizeFirstLetter(string:string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

const ImmaginiPrevisioni: React.FC<Props> = ({ previsioni }) => {
    if (!previsioni) return (<div className='text-bold'>Loading previsions or not avialable yet for your apartment.</div>);
    return (
        <div>
            {Object.keys(previsioni).map((key: string, index) => (
                <div key={index} className='my-6'>
                    <div className='text-center font-bold my-6'>{capitalizeFirstLetter(key)}</div>
                    <img key={index} src={`data:image/png;base64,${previsioni[key]}`} alt={key} />
                </div>
            ))}
        </div>
    );
};
//                 <span key={index}> {key} {previsioni[key]} </span>


export default ImmaginiPrevisioni;
