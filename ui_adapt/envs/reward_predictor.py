import pickle
import os
import pandas as pd

class RewardPredictor:
    def __init__(self, filename):
        self.number_of_decimals = 4    
        current_folder = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(current_folder, filename)
        print(f"model path {filename}")
        self.model = pickle.load(open(model_path, 'rb'))

    def predict(self, data):
        data = self.prepare_data(data)
        predictions = self.model.predict(data)

        # Apply rounding to avoid large number of decimals
        # Apply also x1.5 scaling to fit rewards with the 0 to 1 values.
        for i, prediction in enumerate(predictions):
            predictions[i] = predictions[i] * 2 if predictions[i] * 1.5 <= 1 else 1
            predictions[i] = round(predictions[i], self.number_of_decimals)
        return predictions
    
    def prepare_data(self,data):
        # data is the pointer to the UIDesign class instantiation
        data_columns = ['theme_dark', 'theme_light', 'display_grid', 'display_list']
        data_values = []
        if data.theme == 'light':
            data_values.extend([0,1])
        elif data.theme == 'dark':
            data_values.extend([1,0])
        if 'grid' in data.layout:
            data_values.extend([1,0])
        elif data.layout == 'list':
            data_values.extend([0,1])
        
        # Create a new DataFrame for making predictions
        new_data = pd.DataFrame([data_values], columns=data_columns)
        return new_data

    def get_alignment(self, user, uidesign):
        # How different are the user preferences and the uidesign.
        
        max_alignment = len(user.preferences)

        alignment = max_alignment  # Start with the maximum alignment

        for attribute, attribute_value in uidesign.attributes.items():
            user_value = user.preferences.get(attribute, "").lower()
            attribute_value_lower = attribute_value.lower()
            if user_value != attribute_value_lower:
                alignment -= 1
         # Normalize alignment score to be between 0 and 1
        normalized_alignment = alignment / max_alignment
        return normalized_alignment