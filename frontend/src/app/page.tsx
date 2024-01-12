"use client";

import { useEffect, useState } from 'react';
import { Button } from "@/components/ui/button";
import { CardContent, Card } from "@/components/ui/card";

type TownRead = {
  id: number;
  name: string;
  population: number;
  country: string;
  // Add other fields as needed
};

type PeopleRead = {
  id: number;
  name: string;
  gender: string;
  age: string;
  // Add other fields as needed
};

const TownData = () => {
  const [townData, setTownData] = useState<TownRead[] | null>(null);
  const [peopleData, setPeopleData] = useState<PeopleRead[] | null>(null);

  useEffect(() => {
    // Fetch town data from your FastAPI endpoint
    fetch('http://localhost:8000/towns/')
      .then(response => response.json())
      .then(data => setTownData(data))
      .catch(error => console.error('Error fetching town data:', error));

    // Fetch people data from your FastAPI endpoint
    fetch('http://localhost:8000/people/')
      .then(response => response.json())
      .then(data => setPeopleData(data))
      .catch(error => console.error('Error fetching people data:', error));
  }, []);

  if (!townData || !peopleData) {
    return "API Resolution Error!"; // or a loading indicator
  }

  return (
    <div className="flex flex-col min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100">
      <header className="flex items-center justify-between p-6 border-b dark:border-gray-800">
        <h1 className="text-2xl font-bold">Town & People Data</h1>
        <Button className="dark:border-gray-300" variant="outline">
          Refresh Data
        </Button>
      </header>
      <main className="flex-1 overflow-auto p-6">
        <section className="mb-8">
          <h2 className="text-xl font-semibold mb-4">Town Data</h2>
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {Array.isArray(townData) ? (
              townData.map(town => (
                <Card key={town.id}>
                  <CardContent className="space-y-2">
                    <h3 className="text-lg font-semibold">{town.name}</h3>
                    <p className="text-gray-500 dark:text-gray-400">Population: {town.population}</p>
                    {/* Add other town-related information here */}
                  </CardContent>
                </Card>
              ))
            ) : (
              <p>No town data available</p>
            )}
          </div>
        </section>
        <section>
          <h2 className="text-xl font-semibold mb-4">People Data</h2>
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {Array.isArray(peopleData) ? (
              peopleData.map(person => (
                <Card key={person.id}>
                  <CardContent className="space-y-2">
                    <h3 className="text-lg font-semibold">{person.name}</h3>
                    <p className="text-gray-500 dark:text-gray-400">Age: {person.age}</p>
                    <p className="text-gray-500 dark:text-gray-400">Gender: {person.gender}</p>
                    {/* Add other person-related information here */}
                  </CardContent>
                </Card>
              ))
            ) : (
              <p>No people data available</p>
            )}
          </div>
        </section>
      </main>
      <footer className="p-6 border-t dark:border-gray-800">
        <p className="text-center text-sm text-gray-500 dark:text-gray-400">
          © 2024 Town & People Data. All rights reserved.
        </p>
      </footer>
    </div>
  );
};

export default TownData;
