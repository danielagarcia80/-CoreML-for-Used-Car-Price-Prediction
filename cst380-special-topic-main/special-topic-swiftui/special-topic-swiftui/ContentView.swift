//
//  ContentView.swift
//  special-topic-swiftui
//
//  Created by Mac on 3/17/25.
//

import SwiftUI
import CoreML

struct ContentView: View {
    @State private var odometer: String = ""
    @State private var year: String = ""
    @State private var condition: Double = 2
    @State private var prediction: String = ""
    @FocusState private var focusedField: Field?

    enum Field {
        case odometer, year
    }

    var body: some View {
        NavigationView {
            ZStack {
                Color(.systemBackground).ignoresSafeArea()

                VStack(spacing: 20) {
                    VStack(alignment: .leading, spacing: 12) {
                        Text("Enter Car Details")
                            .font(.headline)

                        TextField("Odometer (e.g., 45000)", text: $odometer)
                            .keyboardType(.decimalPad)
                            .textFieldStyle(RoundedBorderTextFieldStyle())
                            .focused($focusedField, equals: .odometer)
                            .submitLabel(.next)
                            .onSubmit { focusedField = .year }

                        TextField("Year (e.g., 2018)", text: $year)
                            .keyboardType(.numberPad)
                            .textFieldStyle(RoundedBorderTextFieldStyle())
                            .focused($focusedField, equals: .year)
                            .submitLabel(.done)

                        Text("Condition")
                            .font(.subheadline)
                            .foregroundColor(.secondary)

                        Picker("", selection: $condition) {
                            Text("Salvage").tag(0.0)
                            Text("Fair").tag(1.0)
                            Text("Good").tag(2.0)
                            Text("Excellent").tag(3.0)
                            Text("New").tag(4.0)
                        }
                        .pickerStyle(SegmentedPickerStyle())
                    }
                    .padding()
                    .background(Color(.secondarySystemBackground))
                    .cornerRadius(12)
                    .shadow(color: Color.primary.opacity(0.1), radius: 3)
                    .padding(.horizontal)

                    Button(action: {
                        hideKeyboard()
                        predictPrice()
                    }) {
                        Text("Predict Price")
                            .frame(maxWidth: .infinity)
                            .padding()
                            .background(Color.accentColor)
                            .foregroundColor(.white)
                            .cornerRadius(10)
                    }
                    .padding(.horizontal)

                    VStack(spacing: 10) {
                        Text("Estimated Price")
                            .font(.headline)

                        Text(prediction)
                            .font(.system(size: 32, weight: .bold))
                            .foregroundColor(prediction.starts(with: "$") ? .green : .red)
                            .multilineTextAlignment(.center)
                    }
                    .padding()
                    .frame(maxWidth: .infinity)
                    .background(Color(.secondarySystemBackground))
                    .cornerRadius(12)
                    .shadow(color: Color.primary.opacity(0.1), radius: 3)
                    .padding(.horizontal)

                    Spacer()
                }
                .padding(.top)
                .onTapGesture {
                    hideKeyboard()
                }
            }
            .navigationTitle("Used Car Estimator")
        }
    }

    func predictPrice() {
        guard let odom = Double(odometer), odom >= 0 else {
            prediction = "Please enter a valid odometer value."
            return
        }

        guard let yr = Double(year) else {
            prediction = "Please enter a valid year."
            return
        }

        let currentYear = Double(Calendar.current.component(.year, from: Date()))
        guard yr <= currentYear, yr >= 1950 else {
            prediction = "Year must be between 1950 and \(Int(currentYear))."
            return
        }

        let carAge = currentYear - yr

        do {
            let config = MLModelConfiguration()
            let model = try tree_model(configuration: config)

            let input = tree_modelInput(
                odometer: odom,
                condition: condition,
                year: yr,
                car_age: carAge
            )

            let result = try model.prediction(input: input)
            prediction = "$\(String(format: "%.2f", result.price))"
        } catch {
            prediction = "Prediction failed: \(error.localizedDescription)"
        }
    }

    private func hideKeyboard() {
        UIApplication.shared.sendAction(#selector(UIResponder.resignFirstResponder), to: nil, from: nil, for: nil)
    }
}
