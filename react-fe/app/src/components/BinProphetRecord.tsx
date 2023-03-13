import React from "react";

export const BinProphetRecord = (props: {filling:number, sort_type: string, date: string, color: string }) => {
    return (
        <div className="mx-4">
            <div className="w-full bg-gray-200 rounded-full dark:bg-gray-700">
                <div className={`${props.color} text-xs font-medium text-blue-100 text-center p-0.5 leading-none rounded-full}`} style={{ width:`${( props.filling*100)}%` } }>
                    {(props.filling*100).toFixed(2)}%
                </div>
            </div>
            <div className="text-right mt-4 italic">Estimated filling: {(new Date(props.date).toDateString())}</div>
        </div>
    );

}