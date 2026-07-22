from database_connection import (
    get_database_connection
)

from logger_config import (
    application_logger,
    exception_logger
)


def add_doctor():

    connection = None
    cursor = None

    try:

        doctor_id = input(
            "Enter Doctor ID: "
        ).strip()

        doctor_name = input(
            "Enter Doctor Name: "
        ).strip()

        specialization = input(
            "Enter Specialization: "
        ).strip()

        contact_number = input(
            "Enter Contact Number: "
        ).strip()

        consultation_fee = float(
            input(
                "Enter Consultation Fee: "
            )
        )

        connection = get_database_connection()

        if connection is None:
            return

        cursor = connection.cursor()

        check_query = """
        SELECT doctor_id
        FROM doctors
        WHERE doctor_id = %s
        """

        cursor.execute(
            check_query,
            (doctor_id,)
        )

        if cursor.fetchone() is not None:

            print(
                "Doctor already exists."
            )

            return

        insert_query = """
        INSERT INTO doctors
        (
            doctor_id,
            doctor_name,
            specialization,
            contact_number,
            consultation_fee
        )
        VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(
            insert_query,
            (
                doctor_id,
                doctor_name,
                specialization,
                contact_number,
                consultation_fee
            )
        )

        connection.commit()

        print(
            "Doctor added successfully."
        )

        application_logger.info(
            "Doctor %s added successfully.",
            doctor_id
        )

    except ValueError as error:

        print(
            "Invalid fee."
        )

        exception_logger.exception(
            "Invalid doctor input: %s",
            error
        )

    except Exception as error:

        print(
            "Error while adding doctor:",
            error
        )

        exception_logger.exception(
            "Doctor addition error: %s",
            error
        )

    finally:

        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


def view_all_doctors():

    connection = None
    cursor = None

    try:

        connection = get_database_connection()

        if connection is None:
            return

        cursor = connection.cursor(
            dictionary=True
        )

        cursor.execute(
            "SELECT * FROM doctors"
        )

        doctors = cursor.fetchall()

        if len(doctors) == 0:

            print(
                "No doctors found."
            )

            return

        for doctor in doctors:

            print("\n" + "-" * 50)

            for key, value in doctor.items():

                print(
                    f"{key}: {value}"
                )

    except Exception as error:

        print(
            "Error while viewing doctors:",
            error
        )

        exception_logger.exception(
            "Doctor view error: %s",
            error
        )

    finally:

        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()
