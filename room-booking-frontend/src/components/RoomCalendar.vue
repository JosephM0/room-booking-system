<template>
    <div class="mb-3 text-center">
        <span
            class="badge px-3 py-2"
            :class="isEditor ? 'bg-primary' : 'bg-secondary'"
        >
            {{ roleTitle }}
        </span>
    </div>
    <div>
        <div class="d-flex justify-content-between mb-3">
            <button class="btn btn-secondary" @click="prev">Previous</button>
            <h5>{{ formattedRange }}</h5>
            <button class="btn btn-secondary" @click="next">Next</button>

        </div>

        <table class="table table-bordered text-center align-middle">
            <thead class="table-light">
                <tr>
                    <th>Room</th>
                    <th v-for="date in dates" :key="date">{{ formatDate(date) }}</th>

                </tr>
            </thead>
            <tbody>
                <tr v-for="room in rooms" :key="room.id">
                    <td>{{ room.name }}</td>
                    <td
                        v-for="date in dates"
                        :key="room.id + '-' + date"
                        :class="getBookingClass(room.id, date)"
                        style="cursor: pointer;"
                        @click="isEditor && openBookingModal(room, date)"
                        :style="{ cursor: isEditor ? 'pointer' : 'not-allowed' }"
                    >
                        <span>{{ getBookingLabel(room.id, date) }}</span>
                    </td>
                </tr>
            </tbody>
        </table>

        <div class="modal fade" id="bookingModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">{{ modalTitle }}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>

                    </div>
                    <div class="modal-body">
                        <input
                            v-model="bookingForm.guest_name"
                            class="form-control mb-2"
                            placeholder="Guest name"
                        />
                        <label>Start Date</label>
                        <input
                            type="date"
                            v-model="bookingForm.start_date"
                            class="form-control mb-2"
                        />
                        <label>End Date</label>
                        <input
                            type="date"
                            v-model="bookingForm.end_date"
                            class="form-control mb-2"
                        />
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                            Cancel
                        </button>
                        <button
                            v-if="isEditor"
                            type="button"
                            class="btn btn-sm btn-danger"
                            @click="deleteBooking()"
                        >
                            Delete
                        </button>
                        <button
                            v-if="isEditor"
                            class="btn btn-primary"
                            @click="saveBooking"
                        >
                            {{ isEditing ? "Update" : "Save" }}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import * as bootstrap from "bootstrap";
import { authHeaders, refreshAccessTokens } from "../services/auth";

export default{
    props: {
        userGroups: {
            type: Array,
            default: () => []
        }
    },
    data() {
        return {
            rooms: [],
            bookings: [],
            currentStart: new Date(),
            bookingForm: {},
            modalTitle: "",
            isEditing: false,
        };
    },

    computed: {
        isEditor() {
            return Array.isArray(this.userGroups) && this.userGroups.includes("Receptionist");
        },

        isViewer() {
            if (!Array.isArray(this.userGroups)) return false;

            return this.userGroups.map(g => g.toLowerCase()).includes("marketing");
        },

        roleTitle() {
            if (!Array.isArray(this.userGroups)) return "";

            const groups = this.userGroups.map(g => g.toLowerCase());

            if (groups.includes("receptionist")) {
                return "Receptionist";
            }

            if (groups.includes("marketing")) {
                return "Marketing (View Only)"
            }

            return "User"
        },

        dates() {
            const arr = [];
            const start = new Date(this.currentStart);
            for (let i=0; i<30; i++){
                const d = new Date(start);
                d.setDate(start.getDate() + i);
                arr.push(d.toISOString().split("T")[0]);
            }
            return arr;
        },

        formattedRange() {
            const end = new Date(this.currentStart);
            end.setDate(end.getDate() + 29);
            return `${this.formatDate(this.currentStart)} - ${this.formatDate(end)}`;
        },
    },
    methods: {
        showModal() {
            const modalEL = document.getElementById("bookingModal");
            const modal = new bootstrap.Modal(modalEL);
            modal.show();
        },

        async fetchRooms() {
            const res = await fetch("http://127.0.0.1:8000/api/rooms/", {
                headers: authHeaders()
            });

            if (res.status === 401) {
                await refreshAccessTokens();
                res = await fetch("http://127.0.0.1:8000/api/rooms/", {
                    headers: authHeaders()
                })
            }

            if (!res.ok) {
                console.error("Failed rooms:", await res.text());
                return;
            }

            this.rooms = await res.json();
        },

        async fetchBookings() {
            const res = await fetch("http://127.0.0.1:8000/api/bookings/", {
                headers: authHeaders()
            });

            if(res.status === 401){
                await refreshAccessTokens();
                res = await fetch("http://127.0.0.1:8000/api/bookings/", {
                    headers: authHeaders()
                })
            }

            if (!res.ok) {
                console.error("Failed bookings:", await res.text());
                return;
            }

            const data = await res.json();
            this.bookings = Array.isArray(data) ? data : [];
        },

        formatDate(d) {
            const date = new Date(d);
            return date.toLocaleDateString("en-GB", { day: "numeric", month: "short" });
        },

        getBooking(roomID, date) {
            return this.bookings.find(
                (b) => b.room === roomID && b.start_date <= date && b.end_date >= date
            );
        },

        getBookingClass(roomID, date) {
            const booking = this.getBooking(roomID, date);
            return booking ? "bg-danger text-white" : "bg-success text-white";
        },

        getBookingLabel(roomID, date) {
            const booking = this.getBooking(roomID, date);
            return booking ? booking.guest_name : "Available";
        },

        openBookingModal(room, date) {
            if (!this.isEditor) return;

            const existing = this.getBooking(room.id, date);
            if(existing){
                this.isEditing = true;
                this.bookingForm = { ...existing };
                this.modalTitle = `Edit booking for ${room.name}`;
            } else {
                this.isEditing = false;
                this.bookingForm = {
                    room: room.id,
                    start_date: date,
                    end_date: date,
                    guest_name: "",
                };
                this.modalTitle = `Book ${room.name}`;
            }
            this.showModal();
        },

        async saveBooking() {
            const formatDate = (date) => new Date(date).toISOString().split("T")[0];
            this.bookingForm.start_date = formatDate(this.bookingForm.start_date);
            this.bookingForm.end_date = formatDate(this.bookingForm.end_date);

            const url = this.isEditing
                ? `http://127.0.0.1:8000/api/bookings/${this.bookingForm.id}/`
                : "http://127.0.0.1:8000/api/bookings/";
            const method = this.isEditing ? "PUT" : "POST";

            try {
                const response = await fetch(url, {
                    method,
                    headers: authHeaders(),
                    body: JSON.stringify(this.bookingForm),
                });

                if(!response.ok){
                    const errorData = await response.json();
                    console.error("Booking error:", errorData);
                    alert("Booking Failed: " + JSON.stringify(errorData));
                    return;
                }

                const modal = bootstrap.Modal.getInstance(document.getElementById("bookingModal"));
                modal.hide();

                await this.fetchBookings();

            } catch (err) {
                console.error("Unexpected error:", err);
                alert("An unexpected error occurred while saving the booking.");
            }
        },

        async deleteBooking() {
            if (!this.isEditing) return;
            if(!confirm("Are you sure you want to delete this booking?")) return;

            await fetch(`http://127.0.0.1:8000/api/bookings/${this.bookingForm.id}/`, {
                method: "DELETE",
                headers: authHeaders()
            });

            const modal = bootstrap.Modal.getInstance(
                document.getElementById("bookingModal")
            );
            
            modal.hide();
            this.fetchBookings();
        },

        next() {
            this.currentStart.setDate(this.currentStart.getDate() + 30);
            this.currentStart = new Date(this.currentStart);
        },

        prev() {
            this.currentStart.setDate(this.currentStart.getDate() - 30);
            this.currentStart = new Date(this.currentStart);
        },
    },

    mounted() {
        // console.log("User groups:", this.userGroups);
        this.fetchRooms();
        this.fetchBookings();
    }

};
</script>