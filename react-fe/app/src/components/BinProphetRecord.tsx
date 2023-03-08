import React from "react";

export const BinProphetRecord = (props: {sort_type:string, date:string}) => {
    return (
        <div>
            {props.sort_type}
            <div className="w-full bg-gray-200 rounded-full dark:bg-gray-700">
                <div className="bg-blue-600 text-xs font-medium text-blue-100 text-center p-0.5 leading-none rounded-full" style={{ width: "69%" }}>
                    69%
                </div>
            </div>
            <div className="text-right mt-4">Estimated filling:</div>
        </div>
    );

}