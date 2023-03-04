import { useState, useEffect } from "react";
import React from "react";
import User from "../User";
import PersonList from "../PersonList";
import { Person } from "../PersonList";


import { useLocation } from "react-router-dom";
const AdminRecord = () => {
  const [cmn_city, setCommonCity] = useState<string>("Unknown");
  const [apartment_name, setApartmentName] = useState<string>("Loading");
  const [today_date, setTodayDate] = useState<string>("default_user");

  const [people, setPeople] = useState<Person[]>([]);

  const handlePeopleChange = (people: Person[]) => {
    setPeople(people);
  };

  const { state } = useLocation();

  const user = state as User;


  const onApartmentRegister = () => {

    console.dir(people);

  }

  return (
    <div>
      <section className="h-full gradient-form bg-blue-100 md:h-screen overflow-auto	">
        <div className="container py-12 px-6 h-full">
          <div className="flex justify-center items-center flex-wrap h-full g-6 text-gray-800">
            <div className="xl:w-10/12">
              <div className="block bg-white shadow-lg rounded-lg">
                <div className="lg:flex lg:flex-wrap g-0">
                  <div className="lg:w-6/12 px-4 md:px-0">
                    <div className="md:p-12 md:mx-6">
                      <div className="text-left">
                        {/* <img
                                                className="mx-auto w-48"
                                                width="100px"
                                                src=""
                                                alt="logo"
    /> */}
                        <h3 className="text-xl font-semibold mt-2 pt-3 mb-0 pb-1">Apartment {apartment_name}.</h3>

                        <h4 className="text-xl font-semibold mt-1 mb-0 pb-1">
                          Welcome
                        </h4>
                      </div>
                    </div>
                    <h3 className="ml-4 text-xl font-semibold mt-2 pt-3 mb-4 pb-1">First-time apartment registration</h3>
                    <div className="ml-4">
                      <label className='block mb-2 text-sm font-medium text-gray-900 dark:text-white'>
                        Apartment City:
                        <input
                          type="text"
                          className='w-60 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
                          value={cmn_city}
                          onChange={(e) => setCommonCity(e.target.value)}
                        />
                      </label>
                    </div>

                    <PersonList onPeopleChange={handlePeopleChange} ></PersonList>

              <hr className="mt-4 mb-4"></hr>

                    <div className="ml-4">
                      <h2 className="mb-4 font-semibold text-gray-900 dark:text-white">Check which materials the condominium separates</h2>
                      <ul className="w-48 text-sm font-medium text-gray-900 bg-white border border-gray-200 rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white">
                        <li className="w-full border-b border-gray-200 rounded-t-lg dark:border-gray-600">
                          <div className="flex items-center pl-3">
                            <input id="paper-checkbox" type="checkbox" value="" className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-700 dark:focus:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500"/>
                              <label htmlFor="vue-checkbox" className="w-full py-3 ml-2 text-sm font-medium text-gray-900 dark:text-gray-300">Paper</label>
                          </div>
                        </li>
                        <li className="w-full border-b border-gray-200 rounded-t-lg dark:border-gray-600">
                          <div className="flex items-center pl-3">
                            <input id="plastic-checkbox" type="checkbox" value="" className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-700 dark:focus:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500"/>
                              <label htmlFor="react-checkbox" className="w-full py-3 ml-2 text-sm font-medium text-gray-900 dark:text-gray-300">Plastic</label>
                          </div>
                        </li>
                        <li className="w-full border-b border-gray-200 rounded-t-lg dark:border-gray-600">
                          <div className="flex items-center pl-3">
                            <input id="glass-checkbox" type="checkbox" value="" className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-700 dark:focus:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500"/>
                              <label htmlFor="angular-checkbox" className="w-full py-3 ml-2 text-sm font-medium text-gray-900 dark:text-gray-300">Glass</label>
                          </div>
                        </li>
                        <li className="w-full border-b border-gray-200 rounded-t-lg dark:border-gray-600">
                          <div className="flex items-center pl-3">
                            <input id="organic-checkbox" type="checkbox" value="" className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-700 dark:focus:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500"/>
                              <label htmlFor="laravel-checkbox" className="w-full py-3 ml-2 text-sm font-medium text-gray-900 dark:text-gray-300">Organic</label>
                          </div>
                        </li>
                      </ul>
                    </div>




                    <div>
                      <div className="m-4 mb-4 mt-16">Cosa permette di fare questo tool? Spiegaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa</div>

                      <div className="text-center pt-1 mb-12 pb-1">
                        <button onClick={onApartmentRegister} className="inline-block px-6 py-2.5 text-gray font-medium text-xs leading-tight uppercase rounded shadow-md hover:bg-blue-400 hover:shadow-lg focus:shadow-lg focus:outline-none focus:ring-0 active:shadow-lg transition duration-150 ease-in-out w-full mb-3" type="button" data-mdb-ripple="true" data-mdb-ripple-color="light">
                          Register Apartment
                        </button>

                        {/* <a className="text-gray-500" href="#!">Tutto apposto?</a>
                                            
*/}
                      </div>
                    </div>
                  </div>


                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default AdminRecord;
