import type { NextPage } from 'next'
import Head from 'next/head'
import Image from 'next/image'
import { useState, useEffect } from 'react'


const Home: NextPage = () => {
  useEffect(() => {
    import("flowbite/dist/flowbite");
  }, []);
  const [apartment_key, setApartmentKey] = useState(0);
  const [checked_state, setCheck] = useState('a');

  return (
    <section className="h-full gradient-form bg-gray-200 md:h-screen">
      <div className="container py-12 px-6 h-full">
        <div className="flex justify-center items-center flex-wrap h-full g-6 text-gray-800">
          <div className="xl:w-10/12">
            <div className="block bg-white shadow-lg rounded-lg">
              <div className="lg:flex lg:flex-wrap g-0">
                <div className="lg:w-6/12 px-4 md:px-0">
                  <div className="md:p-12 md:mx-6">
                    <div className="text-center">
                      <img
                        className="mx-auto w-48"
                        width="100px"
                        src="https://e7.pngegg.com/pngimages/165/760/png-clipart-s-s-c-napoli-2017-audi-cup-stadio-san-paolo-football-uefa-champions-league-football-ssc-napoli-2017-audi-cup.png"
                        alt="logo"
                      />
                      <h4 className="text-xl font-semibold mt-1 mb-8 pb-1">the smartest bin among the smartest.</h4>
                      <h5 className="text-l font-italic mt-1 mb-8 pb-1">You are trying to initialize the following apartment: </h5>

                    </div>
                    <form>
                      <p className="mb-4">Please access with given credentials</p>
                      <div className="mb-4">
                        <input
                          type="text"
                          className="form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"
                          id="exampleFormControlInput1"
                          placeholder="Admin username"
                        />
                      </div>
                      <div className="mb-4">
                        <input
                          type="password"
                          className="form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"
                          id="exampleFormControlInput1"
                          placeholder="Master password"
                        />
                      </div>
                      <div className="text-center pt-1 mb-12 pb-1">
                        <button
                          className="inline-block px-6 py-2.5 text-gray font-medium text-xs leading-tight uppercase rounded shadow-md hover:bg-blue-400 hover:shadow-lg focus:shadow-lg focus:outline-none focus:ring-0 active:shadow-lg transition duration-150 ease-in-out w-full mb-3"
                          type="button"
                          data-mdb-ripple="true"
                          data-mdb-ripple-color="light"
                        >
                          Log in
                        </button>
                        <div className="form-check form-check-inline">
                          <input className="form-check-input appearance-none h-4 w-4 border border-gray-300 rounded-sm bg-white checked:bg-blue-600 checked:border-blue-600 focus:outline-none transition duration-200 mt-1 align-top bg-no-repeat bg-center bg-contain float-left mr-2 cursor-pointer" type="checkbox" id="inlineCheckbox2" value="option2" />
                          <label className="form-check-label inline-block text-gray-800" htmlFor="inlineCheckbox2">Confirm apartmend id</label>
                        </div>
                        <a className="text-gray-500" href="#!">Tutto apposto?</a>
                      </div>
                      { /** 
                    <div className="flex items-center justify-between pb-6">
                      <p className="mb-0 mr-2">Don't have an account?</p>
                      <button
                        type="button"
                        className="inline-block px-6 py-2 border-2 border-red-600 text-red-600 font-medium text-xs leading-tight uppercase rounded hover:bg-black hover:bg-opacity-5 focus:outline-none focus:ring-0 transition duration-150 ease-in-out"
                        data-mdb-ripple="true"
                        data-mdb-ripple-color="light"
                      >
                        Danger
                      </button>
                    </div>
                  */ }

                    </form>
                  </div>
                </div>
                <div
                  className="lg:w-6/12 flex items-center lg:rounded-r-lg rounded-b-lg lg:rounded-bl-none"
                >
                  <div className="text-black px-4 py-6 md:p-12 md:mx-6">
                    <h4 className="text-xl font-semibold mb-6">We are more than just a bin, let me explain y.</h4>
                    <p className="text-sm">
                      Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
                      tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
                      quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
                      consequat.

                      Spiega che roba è.

                      Bidone fantastico bellissimo me lo sposo guarda eccomi ciao.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

export default Home
