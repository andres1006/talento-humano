import React from "react";
import { Link } from "react-router-dom";

const Dashboard: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Bienvenido al Sistema de Gestión de Talento Humano
        </h1>
        <p className="text-lg text-gray-600">
          Gestiona clientes, candidatos, ofertas laborales y asociaciones de
          manera eficiente
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
          <div className="flex items-center">
            <div className="p-3 rounded-full bg-blue-100 text-blue-600">
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
                />
              </svg>
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-semibold text-gray-900">Clientes</h3>
              <p className="text-gray-600">Gestionar información de clientes</p>
            </div>
          </div>
          <Link
            to="/clientes"
            className="mt-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
          >
            Ver Clientes
          </Link>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
          <div className="flex items-center">
            <div className="p-3 rounded-full bg-green-100 text-green-600">
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                />
              </svg>
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-semibold text-gray-900">
                Candidatos
              </h3>
              <p className="text-gray-600">Administrar candidatos</p>
            </div>
          </div>
          <Link
            to="/candidatos"
            className="mt-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700"
          >
            Ver Candidatos
          </Link>
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Resumen del Sistema
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-gray-600">
          <div>
            <h3 className="font-medium text-gray-900 mb-2">
              Funcionalidades Principales:
            </h3>
            <ul className="space-y-1">
              <li>• Gestión completa de clientes</li>
              <li>• Administración de candidatos</li>
              <li>• Control de ofertas laborales</li>
              <li>• Asociación de candidatos a ofertas</li>
            </ul>
          </div>
          <div>
            <h3 className="font-medium text-gray-900 mb-2">
              Operaciones Disponibles:
            </h3>
            <ul className="space-y-1">
              <li>• Crear nuevos registros</li>
              <li>• Consultar información</li>
              <li>• Modificar datos existentes</li>
              <li>• Inhabilitar registros</li>
            </ul>
          </div>
          <div>
            <h3 className="font-medium text-gray-900 mb-2">Navegación:</h3>
            <ul className="space-y-1">
              <li>• Menú superior para acceso rápido</li>
              <li>• Interfaz intuitiva y responsive</li>
              <li>• Gestión centralizada</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
