import React from "react";


function calculateDateDifference(dueDateStr:string, currentDateStr:string) {
    const dueDate = new Date(dueDateStr);
    const currentDate = new Date(currentDateStr);
    const differenceInDays = Math.ceil((dueDate.getTime() - currentDate.getTime()) / (1000 * 60 * 60 * 24));
    return differenceInDays;
}



export const BinProphetRecord = (props: {filling:number, sort_type: string, date: string, color: string }) => {
    return (
        <div>
            {props.sort_type}
            {props.filling}
            <div className="w-full bg-gray-200 rounded-full dark:bg-gray-700">
                <div className={`${props.color} text-xs font-medium text-blue-100 text-center p-0.5 leading-none rounded-full}`} style={{ width:`${( props.filling*100)}%` } }>
                    {props.filling*100}%
                </div>
            </div>
            <div className="text-right mt-4">Estimated filling: {props.date}</div>
        </div>
    );

}