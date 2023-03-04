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
                        type="text"
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
                        type="number"
                        value={rfid_card}
                        onChange={(e) => setBirthYear(parseInt(e.target.value))}
                    />
                </label>
                <br />
                <label className='block mb-2 text-sm font-medium text-gray-900 dark:text-white'>
                    Telegram Username:
                    <input
                        type="text"
                        className='w-60 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
                        value={telegramUsername}
                        onChange={(e) => setTelegramUsername(e.target.value)}
                    />
                </label>
                <br />
                <button onClick={addPerson}>Add Person</button>
            </div>
            <ul>
                {people.map((person, index) => (
                    <li key={index}>
                        {person.name} {person.surname} () @{person.telegramUsername}
                        <button onClick={() => removePerson(index)}>Remove</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default PersonList;
