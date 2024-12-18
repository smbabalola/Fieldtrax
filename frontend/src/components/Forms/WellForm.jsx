// File: /frontend/src/components/Forms/WellForm.jsx
import React from 'react';
import { useForm } from 'react-hook-form';

const WellForm = ({ initialData, onSubmit, isLoading }) => {
  const { register, handleSubmit, formState: { errors } } = useForm({
    defaultValues: initialData
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Well Name</label>
          <input
            {...register("wellName", { required: "Well name is required" })}
            className="w-full p-2 border rounded-md"
          />
          {errors.wellName && (
            <span className="text-red-500 text-sm">{errors.wellName.message}</span>
          )}
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Well Type</label>
          <select
            {...register("wellType", { required: "Well type is required" })}
            className="w-full p-2 border rounded-md"
          >
            <option value="">Select Well Type</option>
            <option value="oil">Oil</option>
            <option value="gas">Gas</option>
            <option value="water">Water</option>
            <option value="injection">Injection</option>
          </select>
        </div>
      </div>
      <button
        type="submit"
        disabled={isLoading}
        className="bg-blue-500 text-white px-4 py-2 rounded-md"
      >
        {isLoading ? 'Saving...' : 'Save Well'}
      </button>
    </form>
  );
};

export default WellForm;