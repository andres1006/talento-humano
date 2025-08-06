import React from "react";
import { Link, useLocation } from "react-router-dom";

const Header: React.FC = () => {
  const location = useLocation();

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  return (
    <header className="bg-blue-600 text-white shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <h1 className="text-xl font-bold">
              Sistema de Gestión de Talento Humano
            </h1>
          </div>
          <nav className="hidden md:flex space-x-8">
            <Link
              to="/"
              className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                isActive("/")
                  ? "bg-blue-700 text-white"
                  : "text-blue-100 hover:bg-blue-500 hover:text-white"
              }`}
            >
              Dashboard
            </Link>
            <Link
              to="/clientes"
              className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                isActive("/clientes")
                  ? "bg-blue-700 text-white"
                  : "text-blue-100 hover:bg-blue-500 hover:text-white"
              }`}
            >
              Clientes
            </Link>
            <Link
              to="/candidatos"
              className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                isActive("/candidatos")
                  ? "bg-blue-700 text-white"
                  : "text-blue-100 hover:bg-blue-500 hover:text-white"
              }`}
            >
              Candidatos
            </Link>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;
