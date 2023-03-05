import React, { useState } from 'react';

export type Person = {
    name: string;
    surname: string;
    telegramUsername: string;
    password: string;
    rfid_card: string;
    birth_year: number;
    intern_number: number;
};

type Props = {
    onPeopleChange: (people: Person[]) => void;
};

const PersonList = (props: Props) => {
    const [name, setName] = useState('');
    const [surname, setSurname] = useState('');
    const [birth_year, setBirthYear] = useState(0);
    const [intern_number, setInternNumber] = useState(0);
    const [rfid_card, setRfidCard] = useState('');
    const [password, setPassword] = useState('');
    const [telegramUsername, setTelegramUsername] = useState('');
    const [people, setPeople] = useState<Person[]>([]);

    const addPerson = () => {
        const newPerson: Person = {
            name,
            surname,
            telegramUsername,
            password,
            rfid_card,
            birth_year,
            intern_number
        };


        if (!name || !surname || !telegramUsername || !password || !rfid_card || !birth_year || !intern_number) {
            alert('Please fill all the fields');
            return;
        }

        const newPeople = [...people, newPerson];
        setPeople(newPeople);
        if (props.onPeopleChange) {
            props.onPeopleChange(newPeople);
        }
        setName('');
        setSurname('');
        setBirthYear(1900);
        setInternNumber(0);
        setRfidCard('');
        setPassword('');
        setTelegramUsername('');
    };

    const removePerson = (index: number) => {
        const newPeople = [...people];
        newPeople.splice(index, 1);
        setPeople(newPeople);
        if (props.onPeopleChange) {
            props.onPeopleChange(newPeople);
        }
    };

    return (
        <div className='ml-4'>
            <div className='mb-2'>
                <h2>Insert data of <span className='font-bold'>{people.length + 1}º</span> co-occupant:</h2>
            </div>
            <div>
                <label className='block mb-2 text-sm font-medium text-gray-900 dark:text-white'>
                    Name:
                    <input
                        type="text"
                        className='w-60 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                    />
                </label>
                <br />
                <label className='block mb-2 text-sm font-medium text-gray-900 dark:text-white'>
                    Surname:
                    <input
                        type="text"
                        value={surname}
                        className='w-60 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
                        onChange={(e) => setSurname(e.target.value)}
                    />
                </label>
                <br />
                <label className='block mb-2 text-sm font-medium text-gray-900 dark:text-white'>
                    Birth Year:
                    <input
                        className='w-60 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
                        type="number"
                        value={birth_year}
                        onChange={(e) => setBirthYear(parseInt(e.target.value))}
                    />
                </label>                <br />
                <label className='block mb-2 text-sm font-medium text-gray-900 dark:text-white'>
                    Password:
                    <input
                        className='w-60 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </label>                <br />
                <label className='block mb-2 text-sm font-medium text-gray-900 dark:text-white'>
                    Intern Number:
                    <input
                        className='w-60 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
                        type="number"
                        value={intern_number}
                        onChange={(e) => setInternNumber(parseInt(e.target.value))}
                    />
                </label>                <br />
                <label className='block mb-2 text-sm font-medium text-gray-900 dark:text-white'>
                    RFID Card:
                    <input
                        className='w-60 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
                        type="text"
                        value={rfid_card}
                        onChange={(e) => setRfidCard(e.target.value)}
                    />
                </label>
                <br />
                <label className='block mb-2 text-sm font-medium text-gray-900 dark:text-white'>

                    Telegram Username:

                    <div className="flex">
                        <span className="inline-flex items-center px-3 text-sm text-gray-900 bg-gray-200 border border-r-0 border-gray-300 rounded-l-md dark:bg-gray-600 dark:text-gray-400 dark:border-gray-600">
                            @
                        </span>
                        <input onChange={(e) => setTelegramUsername(e.target.value)}
                            value={telegramUsername}
                            type="text" id="website-admin" className="w-40 rounded-none rounded-r-lg bg-gray-50 border text-gray-900 focus:ring-blue-500 focus:border-blue-500 block flex-1 min-w-0 text-sm border-gray-300 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="easy_whistleblower" />
                    </div>

                </label>

                <br />
                <button className='className="focus:outline-none text-white bg-purple-700 hover:bg-purple-800 focus:ring-4 focus:ring-purple-300 font-medium rounded-lg text-sm px-5 py-2.5 mb-2 dark:bg-purple-600 dark:hover:bg-purple-700 dark:focus:ring-purple-900"' onClick={addPerson}>Add Person</button>
            </div>
            <ul>
                {people.map((person, index) => (
                    <li key={index}>
                        [{person.name}, {person.surname}, {person.birth_year}, {person.rfid_card}, {person.password}, {person.intern_number}, @{person.telegramUsername}]
                        <button className='ml-3 focus:outline-none text-white bg-red-700 hover:bg-red-800 focus:ring-4 focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-red-600 dark:hover:bg-red-700 dark:focus:ring-red-900' onClick={() => removePerson(index)}>Remove</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default PersonList;
