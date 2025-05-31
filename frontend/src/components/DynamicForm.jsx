import React from 'react';
import { useForm, Controller } from 'react-hook-form';
import { getActiveFormFields } from '../api/formFields';
import { TextField, Button } from '@mui/material';

export function DynamicForm() {
  const [fields, setFields] = React.useState([]);
  const { control, handleSubmit } = useForm();

  React.useEffect(() => {
    getActiveFormFields().then(setFields);
  }, []);

  const onSubmit = async (data) => {
    alert(JSON.stringify(data));
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {fields.map((field) => (
        <Controller
          key={field.name}
          name={field.name}
          control={control}
          rules={{ required: field.isRequired }}
          render={({ field: { onChange, value } }) => (
            <TextField
              label={field.label}
              type={field.field_type}
              required={field.isRequired}
              value={value || ''}
              onChange={onChange}
              margin="normal"
              fullWidth
            />
          )}
        />
      ))}
      <Button type="submit" variant="contained" color="primary">
        Submit
      </Button>
    </form>
  );
}